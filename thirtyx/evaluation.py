"""
Deterministic ten-lens evaluation for outbound campaign sequences.

[INPUT]: 依赖 campaign sequence JSON、其中的 evidence 与 experiment 定义
[OUTPUT]: 对外提供 evaluate_sequence() 与十维 JSON 评估记录
[POS]: thirtyx 的离线质量门；将硬规则与后续模型辅助审阅明确分离
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import re

from .decision import experiment_errors


PASS_SCORE = 85
FABRICATED_PHRASES = (
    "impressive momentum",
    "been following your journey",
    "your background caught my eye",
    "probably juggling",
)


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def lens(name, checks):
    passed = sum(1 for check in checks if check[0])
    return {
        "name": name,
        "score": round(10 * passed / max(len(checks), 1), 1),
        "checks": [
            {"passed": ok, "message": message}
            for ok, message in checks
        ],
    }


def verified_evidence_ids(evidence):
    return {
        item.get("id") for item in evidence
        if item.get("id") and item.get("verified") is True
    }


def referenced_evidence_ids(steps):
    return {
        evidence_id
        for step in steps
        for evidence_id in step.get("evidence_ids", [])
    }


def opening_token(body):
    opening = re.match(r"\s*([A-Za-z]+)", body)
    return opening.group(1).lower() if opening else ""


def evaluation_context(campaign):
    steps = campaign.get("steps", [])
    experiment = campaign.get("experiment", {})
    verified = verified_evidence_ids(campaign.get("evidence", []))
    bodies = [str(step.get("body", "")) for step in steps]
    subjects = [str(step.get("subject", "")) for step in steps]
    referenced = referenced_evidence_ids(steps)
    first = steps[0] if steps else {}
    first_body = str(first.get("body", ""))
    return {
        "steps": steps, "experiment": experiment, "bodies": bodies,
        "combined": " ".join(subjects + bodies).lower(), "referenced": referenced,
        "unverified": sorted(referenced - verified), "first": first,
        "first_subject": str(first.get("subject", "")), "first_body": first_body,
        "first_token": opening_token(first_body),
        "days": [step.get("day") for step in steps],
        "ctas": [str(step.get("cta", "")).strip() for step in steps],
    }


def hard_blockers(context):
    blockers = []
    fabricated = [phrase for phrase in FABRICATED_PHRASES if phrase in context["combined"]]
    if not context["steps"]:
        blockers.append("sequence has no steps")
    if context["unverified"]:
        blockers.append(f"unverified evidence references: {', '.join(context['unverified'])}")
    if fabricated:
        blockers.append(f"unsupported personalization language: {', '.join(fabricated)}")
    if not context["experiment"].get("hypothesis"):
        blockers.append("experiment hypothesis is missing")
    if not context["experiment"].get("variable"):
        blockers.append("experiment variable is missing")
    if not context["experiment"].get("primary_metric"):
        blockers.append("primary metric is missing")
    blockers.extend(experiment_errors(context["experiment"]))
    return blockers


def targeting_lens(campaign, _context):
    return lens("targeting_context", [
        (bool(campaign.get("audience")), "audience is defined"),
        (bool(campaign.get("anti_icp")), "anti-ICP is explicit"),
    ])


def subject_lens(_campaign, context):
    subject = context["first_subject"]
    return lens("subject_line", [
        (3 <= word_count(subject) <= 7, "first subject uses 3–7 words"),
        ("!" not in subject and subject != subject.upper(), "first subject avoids shouty formatting"),
    ])


def opening_lens(_campaign, context):
    return lens("opening", [
        (context["first_token"] not in {"i", "we", "our"}, "opening does not lead with the sender"),
        (word_count(context["first_body"]) <= 80, "first touch is concise"),
    ])


def evidence_lens(_campaign, context):
    return lens("relevance_evidence", [
        (bool(context["referenced"]), "sequence cites at least one evidence object"),
        (not context["unverified"], "every cited evidence object is verified"),
    ])


def value_lens(campaign, _context):
    return lens("value_proposition", [
        (bool(campaign.get("value_proposition")), "value proposition is explicit"),
        (bool(campaign.get("buyer_problem")), "buyer problem is explicit"),
    ])


def proof_lens(_campaign, context):
    fabricated = any(phrase in context["combined"] for phrase in FABRICATED_PHRASES)
    unresolved = "{{proof" in context["combined"] or "[proof" in context["combined"]
    return lens("proof_integrity", [
        (not fabricated, "copy avoids unsupported familiarity or praise"),
        (not unresolved, "copy has no unresolved proof placeholders"),
    ])


def cta_lens(_campaign, context):
    return lens("cta", [
        (bool(context["first"].get("cta")), "first touch declares a CTA"),
        (all(word_count(cta) <= 12 for cta in context["ctas"] if cta), "every declared CTA is concise"),
        (all(body.count("?") <= 1 for body in context["bodies"]), "each touch asks at most one question"),
    ])


def sequence_lens(_campaign, context):
    days = context["days"]
    return lens("sequence_logic", [
        (all(isinstance(day, int) for day in days), "every step has an integer day"),
        (days == sorted(days) and len(days) == len(set(days)), "sequence days are unique and increasing"),
    ])


def deliverability_lens(_campaign, context):
    return lens("deliverability_compliance", [
        (not re.search(r"https?://", context["first_body"]), "first touch contains no URL"),
        (all(word_count(body) <= 120 for body in context["bodies"]), "every touch stays under 120 words"),
    ])


def measurement_lens(_campaign, context):
    experiment = context["experiment"]
    thresholds = experiment.get("decision_thresholds", {})
    return lens("measurement_learning", [
        (bool(experiment.get("variable")), "single test variable is explicit"),
        (int(experiment.get("minimum_sample_size", 0) or 0) > 0, "minimum sample size is preregistered"),
        (all(key in thresholds for key in ("scale", "kill", "learn")), "SCALE/KILL/LEARN thresholds are explicit"),
    ])


LENS_BUILDERS = (
    targeting_lens, subject_lens, opening_lens, evidence_lens, value_lens,
    proof_lens, cta_lens, sequence_lens, deliverability_lens, measurement_lens,
)


def evaluate_sequence(campaign):
    context = evaluation_context(campaign)
    blockers = hard_blockers(context)
    lenses = [builder(campaign, context) for builder in LENS_BUILDERS]
    score = round(sum(item["score"] for item in lenses), 1)
    return {
        "schema_version": "1.0", "campaign_id": campaign.get("campaign_id", ""),
        "sequence_version": campaign.get("sequence_version", ""),
        "score": score, "pass_score": PASS_SCORE,
        "decision": "READY_FOR_HUMAN_REVIEW" if score >= PASS_SCORE and not blockers else "REVISE",
        "hard_blockers": blockers, "lenses": lenses,
        "model_review": {"status": "NOT_RUN", "note": "Qualitative model review is optional and must remain separate from deterministic checks."},
    }
