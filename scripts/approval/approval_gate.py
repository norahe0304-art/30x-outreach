#!/usr/bin/env python3
"""
[INPUT]: 依赖 payload/manifest JSON 与 thirtyx.approval
[OUTPUT]: 对外提供 create/verify 兼容 CLI
[POS]: scripts/approval 的薄 wrapper；哈希与验证逻辑只存在于 thirtyx package
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import argparse
import json
import sys

from thirtyx.approval import create_manifest, load_json, verify_manifest, write_json


def build_parser():
    parser = argparse.ArgumentParser(description="Create or verify immutable outreach approvals")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("--payload", required=True)
    create.add_argument("--approved-by", required=True)
    create.add_argument("--campaign-id", default="")
    create.add_argument("--output", required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--payload", required=True)
    verify.add_argument("--manifest", required=True)
    return parser


def run_create(args, payload):
    manifest = create_manifest(payload, args.approved_by, args.campaign_id)
    write_json(args.output, manifest)
    print(f"Approved {manifest['recipient_count']} recipients: {manifest['content_sha256']}")
    return 0


def run_verify(args, payload):
    manifest = load_json(args.manifest)
    valid, errors = verify_manifest(payload, manifest)
    if valid:
        print(f"Approval verified: {manifest['content_sha256']}")
        return 0
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1


def main():
    args = build_parser().parse_args()
    try:
        payload = load_json(args.payload)
        return run_create(args, payload) if args.command == "create" else run_verify(args, payload)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
