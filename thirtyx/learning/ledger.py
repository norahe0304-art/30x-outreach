"""
[INPUT]: 依赖 campaign、observation、decision 聚合数据与 canonical SHA-256
[OUTPUT]: 对外提供 append/load/verify/head 的 hash-chain ledger
[POS]: thirtyx 的持久学习记忆；不保存 recipient PII，外部固定 head 后可检测整链重写
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from ..approval import content_sha256
from ..contracts import validate_instance


def load_records(path):
    ledger = Path(path)
    if not ledger.exists():
        return []
    return [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]


def ledger_head(records):
    return records[-1].get("record_sha256", "") if records else ""


def validate_record_inputs(campaign, observation, decision):
    validate_instance(campaign, "campaign-spec.schema.json")
    validate_instance(observation, "experiment-observation.schema.json")
    validate_instance(decision, "decision-record.schema.json")
    if decision.get("campaign_id") != campaign.get("campaign_id"):
        raise ValueError("decision campaign_id does not match campaign")
    if decision.get("sequence_version") != campaign.get("sequence_version"):
        raise ValueError("decision sequence_version does not match campaign")


def record_body(campaign, observation, decision, previous_sha256, recorded_at):
    validate_record_inputs(campaign, observation, decision)
    experiment = campaign["experiment"]
    return {
        "schema_version": "1.0", "recorded_at": recorded_at,
        "previous_sha256": previous_sha256,
        "campaign_id": campaign["campaign_id"], "sequence_version": campaign["sequence_version"],
        "audience": campaign["audience"], "hypothesis": experiment["hypothesis"],
        "variable": experiment["variable"], "observation": observation,
        "decision": decision,
    }


def signed_record(campaign, observation, decision, previous_sha256, recorded_at=None):
    timestamp = recorded_at or datetime.now(timezone.utc).isoformat()
    body = record_body(campaign, observation, decision, previous_sha256, timestamp)
    return {**body, "record_sha256": content_sha256(body)}


def record_contract_errors(record, index):
    contracts = (
        (record, "learning-record.schema.json"),
        (record.get("observation"), "experiment-observation.schema.json"),
        (record.get("decision"), "decision-record.schema.json"),
    )
    errors = []
    for instance, schema in contracts:
        try:
            validate_instance(instance, schema)
        except ValueError as error:
            errors.append(f"record {index}: {error}")
    return errors


def verify_records(records):
    errors = []
    previous = ""
    for index, record in enumerate(records):
        digest = record.get("record_sha256", "")
        body = {key: value for key, value in record.items() if key != "record_sha256"}
        errors.extend(record_contract_errors(record, index))
        if record.get("previous_sha256") != previous:
            errors.append(f"record {index} has a broken previous hash")
        if digest != content_sha256(body):
            errors.append(f"record {index} content hash does not match")
        previous = digest
    return not errors, errors


def append_record(path, campaign, observation, decision, recorded_at=None):
    records = load_records(path)
    valid, errors = verify_records(records)
    if not valid:
        raise ValueError("; ".join(errors))
    previous = records[-1]["record_sha256"] if records else ""
    record = signed_record(campaign, observation, decision, previous, recorded_at)
    validate_instance(record, "learning-record.schema.json")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record
