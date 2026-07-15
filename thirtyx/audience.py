"""
[INPUT]: 依赖 audience batch contract 与 provider 返回的 verification、signal metadata
[OUTPUT]: 对外提供 build_audience_batch()、preflight_audience()、assert_execution_ready()
[POS]: thirtyx 的 recipient 写入门；未验证或无信号的 lead 不得跨越 execute 边界
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from datetime import datetime, timezone

from .contracts import validate_instance


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def normalized_email(lead):
    return str(lead.get("email", "")).strip().lower()


def normalized_lead(lead):
    return {
        "email": normalized_email(lead),
        "first_name": str(lead.get("first_name", "")).strip(),
        "last_name": str(lead.get("last_name", "")).strip(),
        "company_name": str(lead.get("company_name", "")).strip(),
        "verification": dict(lead.get("verification", {})),
        "signals": [dict(signal) for signal in lead.get("signals", [])],
    }


def preflight_audience(batch, expected_campaign_id=""):
    validate_instance(batch, "audience-batch.schema.json")
    if expected_campaign_id and batch["campaign_id"] != expected_campaign_id:
        raise ValueError("audience campaign_id does not match campaign")
    emails = [lead["email"].strip().lower() for lead in batch["leads"]]
    if len(emails) != len(set(emails)):
        raise ValueError("audience contains duplicate recipient emails")
    for lead in batch["leads"]:
        signal_ids = [signal["id"] for signal in lead["signals"]]
        if len(signal_ids) != len(set(signal_ids)):
            raise ValueError("audience lead contains duplicate signal ids")
    return batch


def build_audience_batch(campaign_id, leads, generated_at=None):
    batch = {
        "schema_version": "1.0",
        "campaign_id": campaign_id,
        "generated_at": generated_at or utc_now(),
        "leads": [normalized_lead(lead) for lead in leads],
    }
    return preflight_audience(batch, campaign_id)


def assert_execution_ready(leads, campaign_id):
    return build_audience_batch(campaign_id, leads)
