#!/usr/bin/env python3
# [INPUT]: 读取 consumer repo 的 mounted agent、base role、overlay、workflow 和 run-state ledger。
# [OUTPUT]: 对外提供 dry-run warm-up CLI；打印含 proactive learning verdict 的结构化 readback skeleton，不调用外部系统、不写 provider。
# [POS]: scripts runtime-readiness 校验器；验证任意 runtime 能 boot agent contract 并理解 playbook/readback/proactive GEB 路由。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import yaml

REPO_ROOT: Final = Path(__file__).resolve().parent.parent
TODO_RE: Final = re.compile(r"\bTODO:")


@dataclass(frozen=True)
class ContractError(Exception):
    path: Path
    reason: str

    def __str__(self) -> str:
        return f"{self.path}: {self.reason}"


@dataclass(frozen=True)
class TodoHit:
    path: Path
    line: int
    text: str

    def label(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        return f"{rel}:{self.line}: {self.text.strip()}"


def yaml_block(path: Path, key: str) -> dict:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise ContractError(path, "missing yaml block")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict) or not isinstance(data.get(key), dict):
        raise ContractError(path, f"missing {key}")
    return data[key]


def resolve(root: Path, ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute():
        return path
    return root / path


def require_existing(root: Path, ref: str, owner: Path, label: str) -> Path:
    path = resolve(root, ref)
    if not path.exists():
        raise ContractError(owner, f"missing {label}: {path}")
    return path


def require_ref(root: Path, data: dict, key: str, owner: Path) -> Path:
    ref = data.get(key)
    if not isinstance(ref, str) or not ref.strip():
        raise ContractError(owner, f"missing {key}")
    return require_existing(root, ref, owner, key)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def select_agent(root: Path, requested: str | None) -> Path:
    if requested:
        path = resolve(root, requested)
        if not path.exists():
            raise ContractError(path, "agent file does not exist")
        return path
    targets = sorted((root / "agents").glob("*.agent.md"))
    if len(targets) != 1:
        raise ContractError(root, f"expected exactly one agents/*.agent.md, found {len(targets)}")
    return targets[0]


def select_playbook(agent: dict, requested: str | None, owner: Path) -> tuple[str, dict]:
    playbooks = agent.get("playbooks")
    if not isinstance(playbooks, dict) or not playbooks:
        raise ContractError(owner, "playbooks must be a non-empty map")
    if requested:
        spec = playbooks.get(requested)
        if not isinstance(spec, dict):
            raise ContractError(owner, f"playbook {requested!r} is not mounted")
        return requested, spec
    if len(playbooks) != 1:
        raise ContractError(owner, "multiple playbooks mounted; pass --playbook")
    playbook_id = next(iter(playbooks))
    spec = playbooks[playbook_id]
    if not isinstance(spec, dict):
        raise ContractError(owner, f"playbook {playbook_id!r} has bad shape")
    return playbook_id, spec


def check_workflow(workflow: dict, owner: Path) -> list[str]:
    task_graph = workflow.get("task_graph")
    if not isinstance(task_graph, list) or not task_graph:
        raise ContractError(owner, "workflow_contract.task_graph must be non-empty")
    steps: list[str] = []
    for index, step in enumerate(task_graph, 1):
        if not isinstance(step, dict):
            raise ContractError(owner, f"task_graph[{index}] must be a map")
        name = step.get("step")
        refs = step.get("capability_refs")
        mode = step.get("mode")
        if not isinstance(name, str) or not name:
            raise ContractError(owner, f"task_graph[{index}] missing step")
        if not isinstance(mode, str) or not mode:
            raise ContractError(owner, f"task_graph[{index}] missing mode")
        if not isinstance(refs, list) or not refs:
            raise ContractError(owner, f"task_graph[{index}] missing capability_refs")
        steps.append(name)
    readback = workflow.get("readback")
    if not isinstance(readback, dict) or not isinstance(readback.get("include"), list) or not readback["include"]:
        raise ContractError(owner, "workflow_contract.readback.include must be non-empty")
    gate = workflow.get("proactive_learning_gate")
    if not isinstance(gate, dict) or gate.get("required") is not True:
        raise ContractError(owner, "workflow_contract.proactive_learning_gate.required must be true")
    if not isinstance(gate.get("runtime_must_say"), list) or not gate["runtime_must_say"]:
        raise ContractError(owner, "workflow_contract.proactive_learning_gate.runtime_must_say must be non-empty")
    if not isinstance(gate.get("writeback_policy"), dict):
        raise ContractError(owner, "workflow_contract.proactive_learning_gate.writeback_policy must be a map")
    evidence = workflow.get("evidence_packet")
    if not isinstance(evidence, dict) or "required" not in evidence:
        raise ContractError(owner, "workflow_contract.evidence_packet.required is required")
    return steps


def todo_hits(paths: list[Path]) -> list[TodoHit]:
    hits: list[TodoHit] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        lines = path.read_text(errors="ignore").splitlines()
        for line_no, line in enumerate(lines, 1):
            if TODO_RE.search(line):
                hits.append(TodoHit(path=path, line=line_no, text=line))
    return hits


def dry_run(root: Path, agent_ref: str | None, playbook_ref: str | None, runtime: str) -> dict:
    agent_path = select_agent(root, agent_ref)
    agent = yaml_block(agent_path, "mounted_agent")
    product = agent.get("product_contract")
    if not isinstance(product, dict):
        raise ContractError(agent_path, "missing product_contract")

    role_path = require_ref(root, product, "role", agent_path)
    overlay_path = require_ref(root, product, "tenant_attachment", agent_path)
    work_substrate = require_ref(root, product, "work_substrate", agent_path)
    entrypoints = product.get("entrypoints")
    if not isinstance(entrypoints, list) or not entrypoints:
        raise ContractError(agent_path, "product_contract.entrypoints must be a non-empty list")
    for entrypoint in entrypoints:
        require_existing(root, str(entrypoint), agent_path, "entrypoint")

    playbook_id, playbook = select_playbook(agent, playbook_ref, agent_path)
    workflow_path = require_ref(root, playbook, "workflow_contract", agent_path)
    workflow = yaml_block(workflow_path, "workflow_contract")
    steps = check_workflow(workflow, workflow_path)

    run_state = agent.get("run_state_contract")
    if not isinstance(run_state, dict):
        raise ContractError(agent_path, "missing run_state_contract")
    state_root = require_ref(root, run_state, "root", agent_path)
    if not state_root.is_dir():
        raise ContractError(agent_path, f"run_state_contract.root is not a directory: {state_root}")
    state_runs = require_ref(root, run_state, "run_readbacks", agent_path)
    state_deltas = require_ref(root, run_state, "geb_deltas", agent_path)
    state_memory = require_ref(root, run_state, "tenant_memory", agent_path)
    state_protocol = require_ref(root, run_state, "protocol", agent_path)
    for path, label in [(state_runs, "run_readbacks"), (state_deltas, "geb_deltas")]:
        if not path.is_dir():
            raise ContractError(agent_path, f"run_state_contract.{label} is not a directory: {path}")
    for path, label in [(state_memory, "tenant_memory"), (state_protocol, "protocol")]:
        if not path.is_file():
            raise ContractError(agent_path, f"run_state_contract.{label} is not a file: {path}")
    geb_learning = agent.get("geb_learning")
    if not isinstance(geb_learning, dict):
        raise ContractError(agent_path, "missing geb_learning")
    if geb_learning.get("proactive_readback_required") is not True:
        raise ContractError(agent_path, "geb_learning.proactive_readback_required must be true")
    if not isinstance(geb_learning.get("runtime_must_report"), list) or not geb_learning["runtime_must_report"]:
        raise ContractError(agent_path, "geb_learning.runtime_must_report must be non-empty")
    scan_paths = [
        agent_path,
        role_path,
        overlay_path,
        workflow_path,
        state_root / "AGENTS.md",
        state_memory,
    ]
    todos = [hit.label(root) for hit in todo_hits(scan_paths)]
    status = "pass_with_todos" if todos else "pass"

    return {
        "dry_run_agent": {
            "status": status,
            "root": str(root),
            "agent": rel(root, agent_path),
            "playbook": playbook_id,
            "runtime": runtime,
            "loaded": {
                "role": rel(root, role_path),
                "overlay": rel(root, overlay_path),
                "workflow": rel(root, workflow_path),
                "work_substrate": rel(root, work_substrate),
                "state_ledger": {
                    "root": rel(root, state_root),
                    "run_readbacks": rel(root, state_runs),
                    "geb_deltas": rel(root, state_deltas),
                    "tenant_memory": rel(root, state_memory),
                    "protocol": rel(root, state_protocol),
                },
            },
            "workflow": {
                "id": workflow.get("id", ""),
                "default_mode": workflow.get("default_mode", ""),
                "steps": steps,
            },
            "todos": todos,
            "readback_skeleton": {
                "run_readback": {
                    "id": "dry-run",
                    "mounted_agent": rel(root, agent_path),
                    "playbook": playbook_id,
                    "runtime": {"name": runtime, "surface": "other"},
                    "mode": "dry_run",
                    "approval_state": "not_requested",
                    "evidence_refs": [],
                    "actions": {"proposed": [], "applied": [], "blocked": []},
                    "files_changed": [],
                    "ledger_target": f"{rel(root, state_runs)}/dry-run.readback.yaml",
                    "geb_delta": {
                        "verdict": "no-op",
                        "class": "",
                        "target": "",
                        "path": "",
                        "evidence_ref": "",
                        "reason": "dry-run only; no reusable learning persisted",
                        "safety_check": "no credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed tenant facts",
                    },
                    "final_readback": "",
                }
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run a mounted agent boot without external side effects.")
    parser.add_argument("--root", default=".", help="consumer repo root")
    parser.add_argument("--agent", default=None, help="mounted agent path relative to --root")
    parser.add_argument("--playbook", default=None, help="mounted playbook id")
    parser.add_argument("--runtime", default="dry-run", help="runtime surface name to report")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        report = dry_run(root, args.agent, args.playbook, args.runtime)
    except ContractError as err:
        print(f"FAIL  {err}", file=sys.stderr)
        return 1
    print(yaml.safe_dump(report, sort_keys=False, allow_unicode=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
