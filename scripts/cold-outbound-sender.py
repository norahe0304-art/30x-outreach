#!/usr/bin/env python3
"""
Human-gated outbound sender with immutable approvals and privacy-safe history.

[INPUT]: 依赖 approved payload、audience batch、approval manifest、环境变量发送凭据与 config_loader.py
[OUTPUT]: 对外提供默认 preview、显式 --execute 发送、限额与去重日志
[POS]: scripts/ 的最终外部写边界；audience 或内容哈希不匹配绝不发送
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import argparse
import hashlib
import json
import os
import re
import smtplib
import sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path

from thirtyx.approval import load_json, verify_manifest
from thirtyx.audience import preflight_audience
from config_loader import get_sending_config, load_config, write_output


DEFAULT_MAX_PER_DAY = 10
DEFAULT_APPROVED_FILE = "./data/cold-outbound-approved.json"
DEFAULT_HISTORY_FILE = "./data/cold-outbound-history.json"
SUSPICIOUS_PATTERNS = (
    r"sk-[a-zA-Z0-9]{20,}",
    r"Bearer [a-zA-Z0-9\-_.]+",
    r"/Users/[a-zA-Z]+/",
    r"password\s*[:=]\s*\S+",
)


def mask_email(email):
    local, separator, domain = email.partition("@")
    if not separator:
        return "***"
    visible = local[:1] if local else ""
    return f"{visible}***@{domain}"


def recipient_hash(email):
    normalized = email.strip().lower().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def validate_outbound(text):
    if not text or not isinstance(text, str):
        return False
    return not any(re.search(pattern, text, re.IGNORECASE) for pattern in SUSPICIOUS_PATTERNS)


def prospects_from_payload(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("prospects"), list):
        return payload["prospects"]
    raise ValueError("approved payload must be a list or contain a prospects list")


def draft_from_prospect(prospect):
    angle = prospect.get("approved_angle", "A")
    draft = prospect.get("angle_drafts", {}).get(angle, {})
    return angle, draft.get("subject", ""), draft.get("body", "")


def load_history(history_path):
    path = Path(history_path)
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as handle:
            history = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []
    return history if isinstance(history, list) else []


def save_history(history, history_path):
    path = Path(history_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)
        handle.write("\n")


def count_sent_today(history):
    today = datetime.now(timezone.utc).date().isoformat()
    return sum(1 for item in history if (item.get("sent_at") or item.get("created_at", "")).startswith(today))


def send_smtp(to, subject, body, settings):
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = f"{settings['sender_name']} <{settings['sender_email']}>"
    message["To"] = to
    with smtplib.SMTP(settings["host"], int(settings["port"])) as server:
        server.starttls()
        server.login(settings["user"], settings["password"])
        server.sendmail(settings["sender_email"], [to], message.as_string())


def sending_settings(config):
    smtp = get_sending_config(config).get("smtp", {})
    sender_email = os.environ.get("SENDER_EMAIL", "")
    return {
        "sender_email": sender_email,
        "sender_name": os.environ.get("SENDER_NAME", ""),
        "host": os.environ.get("SMTP_HOST", smtp.get("host", "smtp.gmail.com")),
        "port": os.environ.get("SMTP_PORT", smtp.get("port", 587)),
        "user": os.environ.get("SMTP_USER", sender_email),
        "password": os.environ.get("SMTP_PASSWORD", ""),
    }


def require_live_authorization(payload, manifest_path):
    if not manifest_path:
        return False, ["--approval-manifest is required with --execute"]
    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as error:
        return False, [f"approval manifest is unreadable: {error}"]
    return verify_manifest(payload, manifest)


def require_execution_audience(payload, audience_path):
    if not audience_path:
        return False, ["--audience-batch is required with --execute"]
    try:
        audience = preflight_audience(load_json(audience_path), payload.get("campaign_id", ""))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return False, [f"audience batch is invalid: {error}"]
    approved_emails = [str(item.get("email", "")).strip().lower() for item in prospects_from_payload(payload)]
    if any("@" not in email for email in approved_emails) or len(approved_emails) != len(set(approved_emails)):
        return False, ["approved payload contains invalid or duplicate recipients"]
    approved = set(approved_emails)
    staged = {lead["email"].strip().lower() for lead in audience["leads"]}
    if approved != staged:
        return False, ["audience recipients do not match approved payload"]
    return True, []


def build_parser():
    parser = argparse.ArgumentParser(description="Preview approved outreach; execute only with a matching approval manifest")
    parser.add_argument("--execute", action="store_true", help="Perform external sends; preview is the default")
    parser.add_argument("--approval-manifest", help="Manifest created by 30x approve")
    parser.add_argument("--audience-batch", help="Verified, signal-backed audience accepted by 30x preflight")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX_PER_DAY)
    parser.add_argument("--approved-file", default=DEFAULT_APPROVED_FILE)
    parser.add_argument("--history-file", default=DEFAULT_HISTORY_FILE)
    return parser


def load_approved_payload(path):
    approved_path = Path(path)
    if not approved_path.exists():
        raise ValueError(f"approved payload not found: {approved_path}")
    payload = load_json(approved_path)
    return payload, prospects_from_payload(payload)


def enforce_authorization(args, payload):
    if not args.execute:
        return
    approval_valid, approval_errors = require_live_authorization(payload, args.approval_manifest)
    audience_valid, audience_errors = require_execution_audience(payload, args.audience_batch)
    if not approval_valid or not audience_valid:
        raise ValueError("; ".join([*approval_errors, *audience_errors]))


def enforce_credentials(execute, settings):
    if execute and not settings["sender_email"]:
        raise ValueError("SENDER_EMAIL is required with --execute")
    if execute and not settings["password"]:
        raise ValueError("SMTP_PASSWORD is required for live SMTP")


def candidate_message(prospect, known_recipients):
    email = str(prospect.get("email", "")).strip().lower()
    if "@" not in email:
        return None
    fingerprint = recipient_hash(email)
    if fingerprint in known_recipients:
        print(f"  SKIP {mask_email(email)}: already sent")
        return None
    angle, subject, body = draft_from_prospect(prospect)
    if not validate_outbound(subject) or not validate_outbound(body):
        print(f"  BLOCK {mask_email(email)}: missing or suspicious content")
        return None
    return {"email": email, "fingerprint": fingerprint, "angle": angle, "subject": subject, "body": body}


def deliver_message(message, execute, settings):
    if not execute:
        print(f"  PREVIEW {mask_email(message['email'])}: {message['subject']}")
        return True
    try:
        send_smtp(message["email"], message["subject"], message["body"], settings)
    except (OSError, smtplib.SMTPException) as error:
        print(f"  ERROR {mask_email(message['email'])}: {type(error).__name__}", file=sys.stderr)
        return False
    print(f"  SENT {mask_email(message['email'])}: {message['subject']}")
    return True


def history_entry(message):
    content = f"{message['subject']}\n{message['body']}".encode("utf-8")
    return {
        "recipient_sha256": message["fingerprint"],
        "angle": message["angle"],
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sent_at": None,
    }


def deliver_with_journal(message, settings, history, history_path):
    entry = history_entry(message)
    history.append(entry)
    save_history(history, history_path)
    if not deliver_message(message, True, settings):
        history.remove(entry)
        save_history(history, history_path)
        return False
    entry.update({"status": "sent", "sent_at": datetime.now(timezone.utc).isoformat()})
    save_history(history, history_path)
    return True


def process_batch(prospects, execute, settings, history, limit, history_path=None):
    completed = 0
    known_recipients = {item.get("recipient_sha256") for item in history}
    for prospect in prospects:
        if completed >= limit:
            break
        message = candidate_message(prospect, known_recipients)
        if not message:
            continue
        delivered = deliver_with_journal(message, settings, history, history_path) if execute else deliver_message(message, False, settings)
        if not delivered:
            continue
        known_recipients.add(message["fingerprint"])
        completed += 1
    return completed


def report_run(args, completed, sent_today):
    mode = "executed" if args.execute else "previewed"
    live_total = sent_today + (completed if args.execute else 0)
    print(f"\n{mode.capitalize()} {completed} messages. Daily live total: {live_total}")
    write_output(
        module="cold-outbound-sender",
        summary=f"{mode.capitalize()} {completed} messages",
        data={"mode": mode, "messages": completed, "daily_live_total": live_total, "max_per_day": args.max},
    )


def run(args):
    payload, prospects = load_approved_payload(args.approved_file)
    enforce_authorization(args, payload)
    history = load_history(args.history_file)
    sent_today = count_sent_today(history)
    remaining = max(args.max - sent_today, 0)
    if not remaining:
        print(f"Daily limit reached: {sent_today}/{args.max}")
        return 0
    settings = sending_settings(load_config())
    enforce_credentials(args.execute, settings)
    completed = process_batch(prospects, args.execute, settings, history, remaining, args.history_file)
    report_run(args, completed, sent_today)
    return 0


def main():
    try:
        return run(build_parser().parse_args())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
