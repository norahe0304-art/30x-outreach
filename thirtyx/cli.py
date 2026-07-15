"""
[INPUT]: 依赖 contracts、评估、决策、审批、learning、provider 与 rendering API
[OUTPUT]: 对外提供 demo/evaluate/decide/approve/verify/record/history/providers/doctor CLI
[POS]: thirtyx 的产品入口；只路由命令，不复制业务规则
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import argparse
import json
import os
import sys
from importlib import resources

from . import __version__
from .approval import create_manifest, load_json, verify_manifest, write_json
from .contracts import validate_instance
from .decision import decide_experiment
from .evaluation import evaluate_sequence
from .learning import append_record, ledger_head, load_records, verify_records
from .providers import default_registry
from .rendering import render_terminal, terminal_text, write_html


def demo_json(name):
    text = resources.files("thirtyx.demo").joinpath(name).read_text(encoding="utf-8")
    return json.loads(text)


def add_demo_parser(commands):
    parser = commands.add_parser("demo", help="Run the complete offline proof path")
    parser.add_argument("--output", default="30x-demo-report.html", help="Shareable HTML report path")
    parser.add_argument("--no-color", action="store_true")
    parser.set_defaults(handler=command_demo)


def add_evaluate_parser(commands):
    parser = commands.add_parser("evaluate", help="Run the deterministic ten-lens quality gate")
    parser.add_argument("campaign")
    parser.add_argument("--output", help="Optional JSON report path")
    parser.set_defaults(handler=command_evaluate)


def add_decide_parser(commands):
    parser = commands.add_parser("decide", help="Apply frozen SCALE/KILL/LEARN thresholds")
    parser.add_argument("campaign")
    parser.add_argument("observation")
    parser.add_argument("--output", help="Optional decision JSON path")
    parser.add_argument("--html", help="Optional shareable HTML report path")
    parser.add_argument("--no-color", action="store_true")
    parser.set_defaults(handler=command_decide)


def add_approval_parsers(commands):
    approve = commands.add_parser("approve", help="Bind human approval to the exact payload hash")
    approve.add_argument("payload")
    approve.add_argument("--by", required=True, dest="approved_by")
    approve.add_argument("--campaign-id", default="")
    approve.add_argument("--output", required=True)
    approve.set_defaults(handler=command_approve)
    verify = commands.add_parser("verify", help="Verify that an approved payload is unchanged")
    verify.add_argument("payload")
    verify.add_argument("manifest")
    verify.set_defaults(handler=command_verify)


def add_learning_parsers(commands):
    record = commands.add_parser("record", help="Append an aggregate decision to the hash-chained ledger")
    record.add_argument("campaign")
    record.add_argument("observation")
    record.add_argument("--ledger", default=".30x/learning.jsonl")
    record.set_defaults(handler=command_record)
    history = commands.add_parser("history", help="Show the local experiment learning history")
    history.add_argument("--ledger", default=".30x/learning.jsonl")
    history.set_defaults(handler=command_history)
    verify = commands.add_parser("verify-ledger", help="Verify the learning ledger hash chain")
    verify.add_argument("--ledger", default=".30x/learning.jsonl")
    verify.add_argument("--expect-head", default="", help="Trusted head hash that detects a full-chain rewrite")
    verify.set_defaults(handler=command_verify_ledger)


def build_parser():
    parser = argparse.ArgumentParser(prog="30x", description="Auditable demand experiments that compound learning")
    parser.add_argument("--version", action="version", version=f"30x {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    add_demo_parser(commands)
    add_evaluate_parser(commands)
    add_decide_parser(commands)
    add_approval_parsers(commands)
    add_learning_parsers(commands)
    commands.add_parser("providers", help="List built-in and plugin providers").set_defaults(handler=command_providers)
    commands.add_parser("doctor", help="Check local safety and provider readiness").set_defaults(handler=command_doctor)
    return parser


def command_demo(args):
    campaign = demo_json("campaign.json")
    observation = demo_json("observation.json")
    validate_instance(campaign, "campaign-spec.schema.json")
    validate_instance(observation, "experiment-observation.schema.json")
    evaluation = evaluate_sequence(campaign)
    decision = decide_experiment(campaign, observation)
    validate_instance(decision, "decision-record.schema.json")
    output = write_html(args.output, campaign, evaluation, decision)
    print(render_terminal(campaign, evaluation, decision, color=not args.no_color and sys.stdout.isatty()))
    print(f"\nShareable report → {output.resolve()}")
    return 0


def command_evaluate(args):
    campaign = validate_instance(load_json(args.campaign), "campaign-spec.schema.json")
    report = evaluate_sequence(campaign)
    print(f"{report['score']:.1f}/100 · {report['decision']}")
    if args.output:
        write_json(args.output, report)
    return 0 if report["decision"] == "READY_FOR_HUMAN_REVIEW" else 1


def command_decide(args):
    campaign = validate_instance(load_json(args.campaign), "campaign-spec.schema.json")
    observation = validate_instance(load_json(args.observation), "experiment-observation.schema.json")
    evaluation = evaluate_sequence(campaign)
    decision = decide_experiment(campaign, observation)
    validate_instance(decision, "decision-record.schema.json")
    print(render_terminal(campaign, evaluation, decision, color=not args.no_color and sys.stdout.isatty()))
    if args.output:
        write_json(args.output, decision)
    if args.html:
        write_html(args.html, campaign, evaluation, decision)
    return 0


def command_approve(args):
    payload = load_json(args.payload)
    manifest = create_manifest(payload, args.approved_by, args.campaign_id)
    validate_instance(manifest, "approval-manifest.schema.json")
    write_json(args.output, manifest)
    print(f"Approved {manifest['recipient_count']} recipients · {manifest['content_sha256']}")
    return 0


def command_verify(args):
    manifest = validate_instance(load_json(args.manifest), "approval-manifest.schema.json")
    valid, errors = verify_manifest(load_json(args.payload), manifest)
    if valid:
        print("Approval verified · payload is unchanged")
        return 0
    for error in errors:
        print(f"ERROR: {terminal_text(error)}", file=sys.stderr)
    return 1


def command_record(args):
    campaign = validate_instance(load_json(args.campaign), "campaign-spec.schema.json")
    observation = validate_instance(load_json(args.observation), "experiment-observation.schema.json")
    decision = decide_experiment(campaign, observation)
    validate_instance(decision, "decision-record.schema.json")
    record = append_record(args.ledger, campaign, observation, decision)
    print(f"Recorded {record['decision']['decision']} · {record['record_sha256']}")
    return 0


def command_history(args):
    records = load_records(args.ledger)
    print("DECISION  CAMPAIGN                 VERSION  RECORDED AT")
    for record in records:
        decision = terminal_text(record["decision"]["decision"])
        campaign = terminal_text(record["campaign_id"])
        version = terminal_text(record["sequence_version"])
        print(f"{decision:<9} {campaign:<24} {version:<8} {terminal_text(record['recorded_at'])}")
    print(f"HEAD      {ledger_head(records) or '(empty)'}")
    return 0


def command_verify_ledger(args):
    records = load_records(args.ledger)
    valid, errors = verify_records(records)
    head = ledger_head(records)
    if args.expect_head and head != args.expect_head:
        valid, errors = False, [*errors, "ledger head does not match trusted head"]
    if valid:
        print(f"Ledger verified · {len(records)} records · head {head or '(empty)'}")
        return 0
    for error in errors:
        print(f"ERROR: {terminal_text(error)}", file=sys.stderr)
    return 1


def command_providers(_args):
    print("CAPABILITY    PROVIDER      WRITE   REQUIRED ENV")
    for info in default_registry().all():
        write = "yes" if info.external_writes else "no"
        capability = terminal_text(info.capability)
        provider = terminal_text(info.name)
        print(f"{capability:<13} {provider:<13} {write:<7} {terminal_text(', '.join(info.env_vars))}")
    return 0


def command_doctor(_args):
    checks = [("Python >= 3.9", sys.version_info >= (3, 9)), ("Demo resources", bool(demo_json("campaign.json")))]
    for info in default_registry(discover=False).all():
        checks.append((f"{info.name} credentials", all(os.environ.get(name) for name in info.env_vars)))
    for label, ready in checks:
        print(f"{'READY' if ready else 'OPTIONAL':<8} {terminal_text(label)}")
    print("\nOffline demo is always available. Provider credentials are only needed for live integrations.")
    return 0


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
        return args.handler(args)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"ERROR: {terminal_text(error)}", file=sys.stderr)
        return 1
