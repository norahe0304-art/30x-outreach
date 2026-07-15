#!/usr/bin/env python3
# [INPUT]: 读取 consumer 的 agents/state/runs/*.readback.yaml（或 --readback 单文件），契约见 run-state-ledger.protocol.md。
# [OUTPUT]: 对外提供运行一致性回放器；把 propose-first / apply 门禁 / 安全 / GEB 路由从"靠自觉的 prose"变成"被审判的不变量"。通过 0，违约 1。
# [POS]: scripts 行为一致性闸门（非结构）；validate_mounted 审契约写得对，本器审一次运行的 readback 做得对。随 scaffolder vendver 进 consumer。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Judge a run's declared readback against the behavioral invariants.

The structural validators prove a contract is well-formed; they cannot prove a
run behaved. This replayer reads the run_readback an agent emits per
run-state-ledger.protocol.md and judges it against the invariants the protocol
states but no static check could reach:

- apply gating: anything applied must carry approval + evidence + final readback;
- no silent success: every run names a reusable-learning verdict;
- verdict completeness: persisted/proposed must name route, target, evidence,
  reason, and safety check;
- no leaked secrets: the readback itself stores no literal credential.

Honest limit: it judges what the readback DECLARES, not ground truth — a lying
readback can pass. But it moves behavioral compliance from "trust the runtime"
to "the run's own record is judged", which is where the soft underbelly was.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# A literal secret = a key naming a credential bound to a high-entropy value.
# Reference forms (${ENV}, vault://, 1password://) and empty strings are allowed;
# the safety-phrase words ("credentials, OAuth tokens, ...") are prose, not values.
SECRET_KEY = re.compile(
    r"(?i)\b([a-z0-9_]*(?:api[_-]?key|secret|passwd|password|private[_-]?key|"
    r"token|bearer|credential)[a-z0-9_]*)\s*[:=]\s*(['\"]?)([^'\"\s]{12,})\2"
)
ALLOWED_VALUE = re.compile(r"^(\$\{|vault://|1password://|<|TODO|\"\"|''$)")
SAFETY_PHRASE = "no credentials"


class Violation(Exception):
    pass


def check_readback(path: Path) -> list[str]:
    raw = path.read_text()
    doc = yaml.safe_load(raw)
    rb = doc.get("run_readback") if isinstance(doc, dict) else None
    if not isinstance(rb, dict):
        return [f"{path.name}: missing run_readback object"]

    v: list[str] = []
    mode = rb.get("mode", "")
    actions = rb.get("actions") or {}
    applied = actions.get("applied") or []
    approval = str(rb.get("approval_state", "")).lower()
    evidence = rb.get("evidence_refs") or []
    final = rb.get("final_readback", "")

    # 1. Apply gating: anything applied must carry approval + evidence + readback.
    did_apply = mode == "apply" or bool(applied)
    if did_apply:
        if "active" not in approval:
            v.append(f"{path.name}: applied without an active approval_state (propose-first broken)")
        if not evidence:
            v.append(f"{path.name}: applied without evidence_refs (no pre-apply evidence)")
        if not str(final).strip():
            v.append(f"{path.name}: applied without a final_readback (no post-apply readback)")

    # 2. No silent success: every run names a reusable-learning verdict.
    geb = rb.get("geb_delta") or {}
    verdict = geb.get("verdict", "")
    if verdict not in {"persisted", "proposed", "no-op"}:
        v.append(f"{path.name}: geb_delta.verdict must be persisted|proposed|no-op (got {verdict!r})")

    # 3. Persisted/proposed must be fully accounted for.
    if verdict in {"persisted", "proposed"}:
        for field in ["class", "target", "evidence_ref", "reason", "safety_check"]:
            if not str(geb.get(field, "")).strip():
                v.append(f"{path.name}: verdict={verdict} but geb_delta.{field} is empty")
        if SAFETY_PHRASE not in str(geb.get("safety_check", "")).lower():
            v.append(f"{path.name}: geb_delta.safety_check must affirm '{SAFETY_PHRASE}...'")

    # 4. No literal secret stored anywhere in the readback.
    for m in SECRET_KEY.finditer(raw):
        if not ALLOWED_VALUE.match(m.group(3)):
            v.append(f"{path.name}: literal secret stored ({m.group(1)}=...) — use a reference form")
            break

    return v


def main() -> int:
    p = argparse.ArgumentParser(description="Judge run readbacks against behavioral invariants.")
    p.add_argument("--root", default=str(REPO_ROOT), help="consumer repo root")
    p.add_argument("--glob", default="agents/state/runs/*.readback.yaml", help="glob for readbacks")
    p.add_argument("--readback", default=None, help="judge a single readback file instead of a glob")
    args = p.parse_args()

    if args.readback:
        targets = [Path(args.readback).resolve()]
    else:
        targets = sorted(Path(args.root).resolve().glob(args.glob))
    if not targets:
        # No runs yet (fresh instance or spec repo) is valid, not a failure.
        print(f"check_run_conformance: no readbacks under {args.glob} (no runs yet, ok)")
        return 0

    violations: list[str] = []
    for path in targets:
        try:
            found = check_readback(path)
        except (yaml.YAMLError, OSError) as err:
            found = [f"{path.name}: unreadable readback ({err})"]
        if found:
            violations += found
        else:
            print(f"ok    {path.name}")

    if violations:
        print("FAIL  run readbacks violate behavioral invariants:", file=sys.stderr)
        print("\n".join(f"  {x}" for x in violations), file=sys.stderr)
        return 1
    print(f"PASS  {len(targets)} run readback(s) conform to the behavioral invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
