#!/usr/bin/env python3
# [INPUT]: 读取 agents/mounted/*.agent.md 的 yaml 块及其 base role 声明；检查 role、tenant attachment、playbook、work_substrate、entrypoints、run-state 和 proactive GEB 引用。
# [OUTPUT]: 对外提供 mounted agent 装配校验器；通过返回 0，违约返回 1 并打印第一个错误。
# [POS]: scripts mounted-agent 校验器，审判 assembled agent 是否接上 role、tenant、work_substrate、state ledger、proactive learning gate，且 mount playbooks ⊆ role playbooks（子集，非相等；role 空声明则显式跳过并留痕）；无 tenant 特例，runtime 不在协议内不校验。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
# Two-repo aware: refs resolve against ROOT. In the protocol repo ROOT is this
# repo; in a consumer repo ROOT is the consumer, where the protocol is vendored
# under protocol/ and instance files live under agents/.
ROOT = REPO_ROOT


class ContractError(Exception):
    pass


def yaml_block(path: Path) -> dict:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise ContractError(f"{path}: missing yaml block")
    return yaml.safe_load(match.group(1))


def resolve_ref(ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute():
        return path
    return ROOT / path


def require_existing(path: Path, label: str, owner: Path) -> None:
    if not path.exists():
        raise ContractError(f"{owner}: missing {label}: {path}")


def role_playbook_ids(role_path: Path) -> set[str]:
    # The role is the product unit; it declares its callable playbook surface.
    # Returns the declared id set, or empty if the role lists none (nothing to
    # enforce against — a role still being filled is not a failure here).
    pkg = yaml_block(role_path).get("role_package", {})
    available = (pkg.get("playbooks") or {}).get("available") or []
    return {p["id"] for p in available if isinstance(p, dict) and "id" in p}


def contains_phrase(items: list, phrase: str) -> bool:
    return any(phrase in str(item) for item in items)


def validate_workflow_gate(workflow_ref: str, agent_path: Path, playbook_id: str) -> None:
    workflow_path = resolve_ref(workflow_ref)
    require_existing(workflow_path, f"playbook {playbook_id} workflow_contract", agent_path)
    workflow = yaml_block(workflow_path).get("workflow_contract")
    if not isinstance(workflow, dict):
        raise ContractError(f"{workflow_path}: missing workflow_contract")
    readback = workflow.get("readback")
    include = readback.get("include") if isinstance(readback, dict) else None
    if not isinstance(include, list) or not include:
        raise ContractError(f"{workflow_path}: workflow_contract.readback.include must be non-empty")
    for phrase in ["reusable learning verdict", "safety check"]:
        if not contains_phrase(include, phrase):
            raise ContractError(f"{workflow_path}: readback.include must mention {phrase}")
    gate = workflow.get("proactive_learning_gate")
    if not isinstance(gate, dict) or gate.get("required") is not True:
        raise ContractError(f"{workflow_path}: proactive_learning_gate.required must be true")
    if gate.get("no_silent_success") is not True:
        raise ContractError(f"{workflow_path}: proactive_learning_gate.no_silent_success must be true")
    if not isinstance(gate.get("runtime_must_say"), list) or not gate["runtime_must_say"]:
        raise ContractError(f"{workflow_path}: proactive_learning_gate.runtime_must_say must be non-empty")
    if not isinstance(gate.get("writeback_policy"), dict):
        raise ContractError(f"{workflow_path}: proactive_learning_gate.writeback_policy must be a map")


def validate_agent(path: Path) -> None:
    agent = yaml_block(path).get("mounted_agent")
    if not isinstance(agent, dict):
        raise ContractError(f"{path}: missing mounted_agent")

    for section in [
        "identity",
        "product_contract",
        "adaptivity_contract",
        "install_contract",
        "detach_contract",
        "boot_sequence",
        "run_state_contract",
        "playbooks",
        "runtime_boundaries",
        "geb_learning",
    ]:
        if section not in agent:
            raise ContractError(f"{path}: missing {section}")

    # Protocol = role + playbook + 回流. A mounted agent points at a base role, a
    # tenant attachment, and a work substrate. Which agent runtime runs it is the
    # user's choice, so no host/runtime field is required or checked here.
    product = agent["product_contract"]
    for key in ["role", "tenant_attachment", "work_substrate"]:
        if key not in product:
            raise ContractError(f"{path}: product_contract missing {key}")
        require_existing(resolve_ref(product[key]), key, path)
    entrypoints = product.get("entrypoints", [])
    if not isinstance(entrypoints, list) or not entrypoints:
        raise ContractError(f"{path}: product_contract.entrypoints must be a non-empty list")
    for ref in entrypoints:
        require_existing(resolve_ref(ref), "entrypoints", path)

    adaptivity = agent["adaptivity_contract"]
    if adaptivity.get("adaptive") is not True:
        raise ContractError(f"{path}: adaptivity_contract.adaptive must be true")
    for key in ["updates_allowed", "updates_forbidden", "promotion_requires"]:
        if not isinstance(adaptivity.get(key), list) or not adaptivity[key]:
            raise ContractError(f"{path}: adaptivity_contract.{key} must be a non-empty list")

    install = agent["install_contract"]
    if install.get("installable") is not True:
        raise ContractError(f"{path}: install_contract.installable must be true")
    for forbidden in ["credentials", "provider account secrets", "live mutation permission"]:
        if forbidden not in install.get("does_not_install", []):
            raise ContractError(f"{path}: install_contract.does_not_install must include {forbidden}")
    for key in ["installs", "install_check"]:
        if not isinstance(install.get(key), list) or not install[key]:
            raise ContractError(f"{path}: install_contract.{key} must be a non-empty list")

    detach = agent["detach_contract"]
    if detach.get("detachable") is not True:
        raise ContractError(f"{path}: detach_contract.detachable must be true")
    for key in ["detaches", "preserves", "removal_readback_required", "blocked_when"]:
        if not isinstance(detach.get(key), list) or not detach[key]:
            raise ContractError(f"{path}: detach_contract.{key} must be a non-empty list")

    boot = agent["boot_sequence"]
    always_read = boot.get("always_read")
    if not isinstance(always_read, list) or not always_read:
        raise ContractError(f"{path}: boot_sequence.always_read must be non-empty")
    for ref in always_read:
        require_existing(resolve_ref(ref), "boot_sequence.always_read", path)

    run_state = agent["run_state_contract"]
    if not isinstance(run_state, dict):
        raise ContractError(f"{path}: run_state_contract must be a map")
    for key in ["root", "run_readbacks", "geb_deltas", "tenant_memory", "protocol"]:
        if key not in run_state:
            raise ContractError(f"{path}: run_state_contract missing {key}")
        target = resolve_ref(run_state[key])
        require_existing(target, f"run_state_contract.{key}", path)
    for key in ["root", "run_readbacks", "geb_deltas"]:
        target = resolve_ref(run_state[key])
        if not target.is_dir():
            raise ContractError(f"{path}: run_state_contract.{key} is not a directory: {target}")
    for key in ["tenant_memory", "protocol"]:
        target = resolve_ref(run_state[key])
        if not target.is_file():
            raise ContractError(f"{path}: run_state_contract.{key} is not a file: {target}")

    geb_learning = agent["geb_learning"]
    if not isinstance(geb_learning, dict):
        raise ContractError(f"{path}: geb_learning must be a map")
    if geb_learning.get("proactive_readback_required") is not True:
        raise ContractError(f"{path}: geb_learning.proactive_readback_required must be true")
    if not isinstance(geb_learning.get("runtime_must_report"), list) or not geb_learning["runtime_must_report"]:
        raise ContractError(f"{path}: geb_learning.runtime_must_report must be a non-empty list")
    if not isinstance(geb_learning.get("route_rules"), dict) or not geb_learning["route_rules"]:
        raise ContractError(f"{path}: geb_learning.route_rules must be a non-empty map")

    playbooks = agent["playbooks"]
    if not isinstance(playbooks, dict) or not playbooks:
        raise ContractError(f"{path}: playbooks must be a non-empty map")
    # Declaration-vs-reference, not tenant branches: mount playbooks ⊆ role
    # playbooks. Completeness (which subset a tenant exposes) is product policy;
    # consistency (no playbook outside the role's surface) is the assembly
    # invariant. Source of truth is the role, so this holds for any role and any
    # tenant — no customer name in the validator.
    declared = role_playbook_ids(resolve_ref(product["role"]))
    if not declared:
        # The skip is a deliberate loose channel for a role still being filled;
        # announce it so a later debugger never mistakes silence for a pass.
        print(f"note  {path.name}: role declares no playbooks (available: []); skipping surface check")
    else:
        undeclared = set(playbooks) - declared
        if undeclared:
            raise ContractError(
                f"{path}: playbooks {sorted(undeclared)} outside the role's surface "
                f"{sorted(declared)} (require mount playbooks ⊆ role playbooks)")
    for playbook_id, spec in playbooks.items():
        workflow = spec.get("workflow_contract")
        if not workflow:
            raise ContractError(f"{path}: playbook {playbook_id} missing workflow_contract")
        validate_workflow_gate(workflow, path, playbook_id)
        if spec.get("default_mode") != "propose":
            raise ContractError(f"{path}: playbook {playbook_id} default_mode must be propose")
        if "approval_required_before" not in spec or "readback_required" not in spec:
            raise ContractError(f"{path}: playbook {playbook_id} missing approval/readback lists")
        if not contains_phrase(spec["readback_required"], "reusable learning verdict"):
            raise ContractError(f"{path}: playbook {playbook_id} readback_required must mention reusable learning verdict")


def main() -> int:
    global ROOT
    parser = argparse.ArgumentParser(description="Validate mounted agent assembly against the protocol.")
    parser.add_argument("--root", default=str(REPO_ROOT),
                        help="repo root to resolve refs against (the consumer repo when the instance lives elsewhere)")
    parser.add_argument("--glob", default="agents/mounted/*.agent.md",
                        help="glob (relative to --root) for mounted agent files")
    args = parser.parse_args()
    ROOT = Path(args.root).resolve()

    targets = sorted(ROOT.glob(args.glob))
    if not targets:
        # A spec/protocol repo carries no live tenant; the assembly proof lives
        # in consumer repos. Empty is valid, not a failure.
        print(f"validate_mounted_agents: no mounted agents under {ROOT}/{args.glob} (spec repo, ok)")
        return 0

    for path in targets:
        try:
            validate_agent(path)
        except ContractError as err:
            print(f"FAIL  {err}", file=sys.stderr)
            return 1
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        print(f"ok    {rel}")

    print(f"PASS  {len(targets)} mounted agent(s) conform")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
