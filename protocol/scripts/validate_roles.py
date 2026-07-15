#!/usr/bin/env python3
# [INPUT]: 读取 agents/roles/*.role.md 的 yaml 块；契约定义来自 agents/protocols/role-package.schema.md。
#          roles/ 是参考 role 库(可 fork 可无视);消费方自有 role 用 validate_mounted_agents 校验装配。
# [OUTPUT]: 对外提供命令行校验器；通过返回 0，违约返回 1 并打印第一个错误。
# [POS]: scripts 唯一真相源校验器，被 scripts/githooks/pre-commit 调用，是 role-package.schema.md 的执行相。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Adaptive Marketing Agent OS 角色包校验器。

role-package.schema.md 描述契约（语义相），本脚本执行契约（机器相）。
两相必须同构：schema 改字段，此处同步；此处改规则，schema 同步。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# ============================================================
# 契约常量 —— 与 role-package.schema.md / capability-boundary.schema.md 对齐
# ============================================================
REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FIELDS = [
    "identity", "purpose", "when_to_use", "inputs", "outputs",
    "role_instructions", "skills", "playbooks", "memory_scope",
    "runtime_requirements", "capability_manifest",
    "lifecycle", "evidence_contract", "approval_policy", "success_criteria",
    "non_goals", "learning_rules", "versioning",
]
ALLOWED_PROFILES = {
    "read_observe",
    "read_observe_propose",
    "propose_only",
    "paid_media_apply_lab_candidate",
    "draft_asset_apply_lab_candidate",
}
BOUNDARY_SCHEMA = "agents/protocols/capability-boundary.schema.md"


class ContractError(Exception):
    """单条契约违约。携带文件路径与原因。"""


# ============================================================
# 解析 —— 从 markdown 抽出首个 yaml 块
# ============================================================
def yaml_block(path: Path) -> dict:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise ContractError(f"{path}: missing yaml block")
    return yaml.safe_load(match.group(1))


# ============================================================
# 校验 —— 单个角色包逐条体检
# ============================================================
def validate_role(path: Path) -> None:
    pkg = yaml_block(path).get("role_package")
    if not isinstance(pkg, dict):
        raise ContractError(f"{path}: missing role_package")

    missing = [k for k in REQUIRED_FIELDS if k not in pkg]
    if missing:
        raise ContractError(f"{path}: missing fields {missing}")

    if "workflow_contract" in pkg:
        raise ContractError(f"{path}: role_package must not include workflow_contract")

    for forbidden in ["tools", "plugins", "host_adapters", "capability_surface", "mcp_boundary", "permissions"]:
        if forbidden in pkg:
            raise ContractError(f"{path}: concrete runtime or legacy capability field '{forbidden}' is forbidden")

    runtime = pkg["runtime_requirements"]
    if runtime.get("binding_owner") != "tenant_overlay_or_workflow":
        raise ContractError(f"{path}: runtime_requirements.binding_owner must be tenant_overlay_or_workflow")
    abstract_surfaces = runtime.get("abstract_surfaces")
    if not isinstance(abstract_surfaces, list) or not abstract_surfaces:
        raise ContractError(f"{path}: runtime_requirements.abstract_surfaces must be a non-empty list")
    if "concrete_bindings_forbidden" not in runtime:
        raise ContractError(f"{path}: runtime_requirements.concrete_bindings_forbidden is required")

    learning = pkg["learning_rules"]
    if not isinstance(learning.get("routes"), dict) or not isinstance(learning.get("promotion_requires"), list):
        raise ContractError(f"{path}: bad learning_rules shape")

    playbooks = pkg["playbooks"]
    if not isinstance(playbooks.get("available"), list) or not playbooks["available"]:
        raise ContractError(f"{path}: playbooks.available must be a non-empty list")
    for playbook in playbooks["available"]:
        for key in ["id", "name", "workflow_contract"]:
            if key not in playbook:
                raise ContractError(f"{path}: playbook entries require '{key}'")

    manifest = pkg["capability_manifest"]
    if manifest.get("boundary_schema") != BOUNDARY_SCHEMA:
        raise ContractError(f"{path}: capability_manifest.boundary_schema must be {BOUNDARY_SCHEMA}")
    if manifest.get("apply_lab_owner") != "workflow":
        raise ContractError(f"{path}: capability_manifest.apply_lab_owner must be 'workflow'")
    surfaces = manifest.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        raise ContractError(f"{path}: capability_manifest.surfaces must be a non-empty map")
    if set(abstract_surfaces) != set(surfaces):
        raise ContractError(f"{path}: runtime_requirements.abstract_surfaces must match capability_manifest.surfaces")
    for surface, spec in surfaces.items():
        if set(spec) != {"profile"}:
            raise ContractError(f"{path}: surface '{surface}' must contain only profile")
        if spec["profile"] not in ALLOWED_PROFILES:
            raise ContractError(f"{path}: unknown capability profile '{spec['profile']}' in '{surface}'")


# ============================================================
# 入口 —— 收集目标、逐个校验、汇报
# ============================================================
def main() -> int:
    targets = sorted((REPO_ROOT / "agents/roles").glob("*.role.md"))
    if not targets:
        print("validate_roles: no reference role packages found", file=sys.stderr)
        return 1

    for path in targets:
        try:
            validate_role(path)
        except ContractError as err:
            print(f"FAIL  {err}", file=sys.stderr)
            return 1
        print(f"ok    {path.relative_to(REPO_ROOT)}")

    print(f"PASS  {len(targets)} role package(s) conform to role-package.schema.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
