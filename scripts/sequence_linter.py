#!/usr/bin/env python3
"""
[INPUT]: 依赖 campaign JSON 与 thirtyx.evaluation.evaluate_sequence
[OUTPUT]: 对外提供兼容脚本入口、JSON 报告与质量门退出码
[POS]: scripts/ 的薄 CLI wrapper；核心评估只存在于 thirtyx package
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import argparse
import json
from pathlib import Path

from thirtyx.approval import write_json
from thirtyx.evaluation import evaluate_sequence


def main():
    parser = argparse.ArgumentParser(description="Evaluate a campaign across ten deterministic lenses")
    parser.add_argument("sequence", help="Path to campaign sequence JSON")
    parser.add_argument("--output", help="Optional path for the JSON report")
    args = parser.parse_args()
    report = evaluate_sequence(json.loads(Path(args.sequence).read_text(encoding="utf-8")))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.output:
        write_json(args.output, report)
    return 0 if report["decision"] == "READY_FOR_HUMAN_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
