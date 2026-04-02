#!/usr/bin/env python3
"""
Cold Outbound Sender — 审核通过后发送邮件

[INPUT]: 依赖 config_loader.py 的 load_config/get_sending_config/write_output
[OUTPUT]: 对外提供邮件发送 + 历史记录
[POS]: scripts/ 的发送脚本，被 SKILL.md Step 8 调用（需人工审批后才运行）
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

Usage:
    python3 cold-outbound-sender.py [--dry-run] [--max N]
    python3 cold-outbound-sender.py --approved-file path/to/approved.json

SMTP config: config.json > environment variables
"""

import argparse
import json
import os
import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

try:
    from config_loader import load_config, get_sending_config, write_output
except ImportError:
    def load_config(): return {}
    def get_sending_config(c): return {}
    def write_output(m, d, **kw): pass


DEFAULT_MAX_PER_DAY = 10
DEFAULT_APPROVED_FILE = "./data/cold-outbound-approved.json"
DEFAULT_HISTORY_FILE = "./data/cold-outbound-history.json"


def validate_outbound(text):
    """Basic validation for outbound content. Returns (ok, text)."""
    if not text or not isinstance(text, str):
        return False, text
    # Check for common leaked credential patterns
    suspicious_patterns = [
        r'sk-[a-zA-Z0-9]{20,}',       # API keys
        r'Bearer [a-zA-Z0-9\-_.]+',    # Auth headers
        r'/Users/[a-zA-Z]+/',          # Local paths
        r'password\s*[:=]\s*\S+',      # Password patterns
    ]
    import re
    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, text
    return True, text


def load_history(history_path):
    if os.path.exists(history_path):
        try:
            with open(history_path) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_history(history, history_path):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)


def count_sent_today(history):
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(1 for h in history if h.get("sent_date", "").startswith(today))


def send_email_smtp(to, subject, body, sender_email, sender_name,
                    smtp_host, smtp_port, smtp_user, smtp_password, dry_run=False):
    """Send via SMTP."""
    ok_subj, subject = validate_outbound(subject)
    ok_body, body = validate_outbound(body)
    if not ok_subj or not ok_body:
        print(f"  🛡️  Email to {to} BLOCKED by validation (suspicious content detected)")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would send to {to}: {subject}")
        return True

    try:
        msg = MIMEText(body, 'plain')
        msg['Subject'] = subject
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = to

        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, [to], msg.as_string())

        print(f"  ✅ Sent to {to}: {subject}")
        return True
    except Exception as e:
        print(f"  ❌ Error sending to {to}: {e}", file=sys.stderr)
        return False


def send_email_cli(to, subject, body, sender_email, sender_name, cli_command, dry_run=False):
    """Send via a CLI tool (e.g., gog, msmtp, mailx)."""
    ok_subj, subject = validate_outbound(subject)
    ok_body, body = validate_outbound(body)
    if not ok_subj or not ok_body:
        print(f"  🛡️  Email to {to} BLOCKED by validation (suspicious content detected)")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would send to {to}: {subject}")
        return True

    try:
        # Default CLI pattern: gog gmail send
        cmd = cli_command.split() + [
            "--to", to,
            "--subject", subject,
            "--body", body,
            "--from", f"{sender_name} <{sender_email}>",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✅ Sent to {to}: {subject}")
            return True
        else:
            print(f"  ❌ Failed to send to {to}: {result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  ❌ Error sending to {to}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Cold Outbound Sender")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually send emails")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX_PER_DAY,
                        help=f"Max emails per day (default: {DEFAULT_MAX_PER_DAY})")
    parser.add_argument("--approved-file", default=DEFAULT_APPROVED_FILE,
                        help="Path to approved prospects JSON file")
    parser.add_argument("--history-file", default=DEFAULT_HISTORY_FILE,
                        help="Path to send history JSON file")
    parser.add_argument("--send-method", choices=["smtp", "cli"], default="smtp",
                        help="Send method: smtp or cli (default: smtp)")
    parser.add_argument("--cli-command", default="gog gmail send",
                        help="CLI command for sending (used with --send-method cli)")
    args = parser.parse_args()

    # ── 加载配置 (config.json > env) ──
    config = load_config()
    smtp_cfg = get_sending_config(config).get("smtp", {})

    sender_email = smtp_cfg.get("sender_email") or os.environ.get("SENDER_EMAIL", "")
    sender_name = smtp_cfg.get("sender_name") or os.environ.get("SENDER_NAME", "")
    smtp_host = smtp_cfg.get("host") or os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = smtp_cfg.get("port") or os.environ.get("SMTP_PORT", "587")
    smtp_user = smtp_cfg.get("user") or os.environ.get("SMTP_USER", sender_email)
    smtp_password = smtp_cfg.get("password") or os.environ.get("SMTP_PASSWORD", "")

    if not os.path.exists(args.approved_file):
        print(f"No approved prospects file found at {args.approved_file}")
        sys.exit(0)

    with open(args.approved_file) as f:
        approved = json.load(f)

    history = load_history(args.history_file)
    sent_today = count_sent_today(history)
    remaining = args.max - sent_today

    if remaining <= 0:
        print(f"Already sent {sent_today} emails today (max {args.max}). Stopping.")
        sys.exit(0)

    sent_count = 0
    for prospect in approved:
        if sent_count >= remaining:
            break

        email = prospect.get("email")
        if not email or email == "Unknown":
            continue

        # Check if already sent
        if any(h.get("email") == email for h in history):
            print(f"  SKIP {email}: already in history")
            continue

        angle_key = prospect.get("approved_angle", "A")
        drafts = prospect.get("angle_drafts", {})
        draft = drafts.get(angle_key, {})

        subject = draft.get("subject", f"Quick question for {prospect.get('company', 'you')}")
        body = draft.get("body", "")

        if not body:
            print(f"  SKIP {email}: no draft body for angle {angle_key}")
            continue

        if args.send_method == "smtp":
            if not smtp_password and not args.dry_run:
                print("ERROR: SMTP_PASSWORD env var required for smtp sending.")
                sys.exit(1)
            success = send_email_smtp(
                email, subject, body, sender_email, sender_name,
                smtp_host, smtp_port, smtp_user, smtp_password, args.dry_run
            )
        else:
            success = send_email_cli(
                email, subject, body, sender_email, sender_name,
                args.cli_command, args.dry_run
            )

        if success:
            history.append({
                "company": prospect.get("company", ""),
                "contact_name": prospect.get("contact_name", ""),
                "email": email,
                "angle": angle_key,
                "subject": subject,
                "sent_date": datetime.now().isoformat(),
                "score": prospect.get("score", 0),
            })
            sent_count += 1

    if not args.dry_run:
        save_history(history, args.history_file)

    # Remove sent prospects from approved file
    if not args.dry_run and sent_count > 0:
        sent_emails = {h["email"] for h in history}
        remaining_approved = [p for p in approved if p.get("email") not in sent_emails]
        with open(args.approved_file, 'w') as f:
            json.dump(remaining_approved, f, indent=2)

    print(f"\nSent {sent_count} emails ({'dry run' if args.dry_run else 'live'}). Total today: {sent_today + sent_count}")

    # ── 统一格式输出 (30x) ──
    write_output(
        module="cold-outbound-sender",
        summary=f"Sent {sent_count} emails ({'dry run' if args.dry_run else 'live'})",
        data={
            "sent": sent_count,
            "total_today": sent_today + sent_count,
            "dry_run": args.dry_run,
            "max_per_day": args.max,
        },
    )


if __name__ == "__main__":
    main()
