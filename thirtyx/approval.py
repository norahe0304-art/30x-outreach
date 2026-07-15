"""
[INPUT]: 依赖 JSON-compatible payload、审批身份与标准库 hashlib/json
[OUTPUT]: 对外提供 canonical_json、content_sha256、create_manifest、verify_manifest
[POS]: thirtyx 核心安全边界；外部执行只信任与 payload 完全匹配的 manifest
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0"


def canonical_json(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def content_sha256(payload):
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def recipient_count(payload):
    if isinstance(payload, list):
        return len(payload)
    prospects = payload.get("prospects", []) if isinstance(payload, dict) else []
    return len(prospects) if isinstance(prospects, list) else 0


def campaign_id(payload):
    return payload.get("campaign_id", "") if isinstance(payload, dict) else ""


def create_manifest(payload, approved_by, requested_campaign_id=""):
    if not approved_by.strip():
        raise ValueError("approved_by is required")
    payload_campaign = campaign_id(payload)
    if requested_campaign_id and payload_campaign and requested_campaign_id != payload_campaign:
        raise ValueError("campaign_id does not match payload")
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": requested_campaign_id or payload_campaign,
        "approved_by": approved_by.strip(),
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "content_sha256": content_sha256(payload),
        "recipient_count": recipient_count(payload),
    }


def verify_manifest(payload, manifest):
    checks = (
        (manifest.get("schema_version") == SCHEMA_VERSION, "unsupported schema_version"),
        (bool(manifest.get("approved_by")), "approved_by is missing"),
        (bool(manifest.get("approved_at")), "approved_at is missing"),
        (manifest.get("recipient_count") == recipient_count(payload), "recipient_count does not match payload"),
        (not campaign_id(payload) or manifest.get("campaign_id") == campaign_id(payload), "campaign_id does not match payload"),
        (manifest.get("content_sha256") == content_sha256(payload), "content_sha256 does not match payload"),
    )
    errors = [message for valid, message in checks if not valid]
    return not errors, errors


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, payload):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
