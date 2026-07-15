"""
[INPUT]: 依赖 campaign experiment 的结构化阈值与 observation metrics
[OUTPUT]: 对外提供 decide_experiment() 的 COLLECT/SCALE/KILL/LEARN 决策记录
[POS]: thirtyx 的确定性学习引擎；冻结阈值后才解释结果
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import operator


OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

LOWER = {"<", "<="}
HIGHER = {">", ">="}


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def valid_rule(rule):
    return isinstance(rule, dict) and rule.get("operator") in OPERATORS and is_number(rule.get("value"))


def ordered_thresholds(scale, kill):
    if not valid_rule(scale) or not valid_rule(kill):
        return False
    scale_op, kill_op = scale["operator"], kill["operator"]
    if scale_op in HIGHER and kill_op in LOWER:
        return kill["value"] < scale["value"]
    if scale_op in LOWER and kill_op in HIGHER:
        return scale["value"] < kill["value"]
    return False


def experiment_errors(experiment):
    thresholds = experiment.get("decision_thresholds", {})
    thresholds = thresholds if isinstance(thresholds, dict) else {}
    guardrails = experiment.get("guardrails", [])
    errors = []
    if not ordered_thresholds(thresholds.get("scale"), thresholds.get("kill")):
        errors.append("scale and kill thresholds must be valid, opposite, and non-overlapping")
    if thresholds.get("learn") != {"otherwise": True}:
        errors.append("learn threshold must be {'otherwise': true}")
    if not isinstance(guardrails, list) or not all(valid_rule(rule) and rule.get("metric") for rule in guardrails):
        errors.append("every guardrail needs metric, operator, and numeric value")
    sample = experiment.get("minimum_sample_size")
    if not isinstance(sample, int) or isinstance(sample, bool) or sample < 1:
        errors.append("minimum_sample_size must be a positive integer")
    return errors


def validate_experiment(experiment):
    errors = experiment_errors(experiment)
    if errors:
        raise ValueError("; ".join(errors))


def compare(value, rule):
    symbol = rule.get("operator")
    if symbol not in OPERATORS:
        raise ValueError(f"unsupported operator: {symbol}")
    return OPERATORS[symbol](value, rule.get("value"))


def guardrail_failures(metrics, guardrails):
    failures = []
    missing = []
    for rule in guardrails:
        metric = rule.get("metric", "")
        if metric not in metrics:
            missing.append(metric)
        elif not compare(metrics[metric], rule):
            failures.append(metric)
    return failures, missing


def validate_identity(campaign, observation):
    for field in ("campaign_id", "sequence_version"):
        if observation.get(field) != campaign.get(field):
            raise ValueError(f"observation {field} does not match campaign")


def validate_observation(observation):
    sample = observation.get("sample_size")
    metrics = observation.get("metrics")
    if not isinstance(sample, int) or isinstance(sample, bool) or sample < 0:
        raise ValueError("observation sample_size must be a non-negative integer")
    if not isinstance(metrics, dict) or not metrics or not all(is_number(value) for value in metrics.values()):
        raise ValueError("observation metrics must contain numeric values")


def decision_record(campaign, observation, decision, reason, failures=None, missing=None):
    experiment = campaign["experiment"]
    metric = experiment["primary_metric"]
    return {
        "schema_version": "1.0",
        "campaign_id": campaign["campaign_id"],
        "sequence_version": campaign["sequence_version"],
        "decision": decision,
        "reason": reason,
        "sample_size": observation.get("sample_size", 0),
        "primary_metric": metric,
        "primary_value": observation.get("metrics", {}).get(metric),
        "failed_guardrails": failures or [],
        "missing_metrics": missing or [],
    }


def decide_primary(campaign, observation, primary_value, thresholds):
    if compare(primary_value, thresholds["scale"]):
        return decision_record(campaign, observation, "SCALE", "primary metric cleared the scale threshold")
    if compare(primary_value, thresholds["kill"]):
        return decision_record(campaign, observation, "KILL", "primary metric crossed the kill threshold")
    return decision_record(campaign, observation, "LEARN", "result is between the frozen scale and kill thresholds")


def decide_experiment(campaign, observation):
    validate_identity(campaign, observation)
    experiment = campaign["experiment"]
    validate_experiment(experiment)
    validate_observation(observation)
    metrics = observation.get("metrics", {})
    sample_size = observation.get("sample_size", 0)
    failures, missing = guardrail_failures(metrics, experiment.get("guardrails", []))
    if sample_size < experiment["minimum_sample_size"] or missing:
        return decision_record(campaign, observation, "COLLECT", "minimum evidence not reached", failures, missing)
    if failures:
        return decision_record(campaign, observation, "KILL", "a safety guardrail failed", failures)
    primary_value = metrics.get(experiment["primary_metric"])
    if primary_value is None:
        return decision_record(campaign, observation, "COLLECT", "primary metric is missing", missing=[experiment["primary_metric"]])
    return decide_primary(campaign, observation, primary_value, experiment["decision_thresholds"])
