#!/usr/bin/env python3
"""
config_loader.py — 统一配置加载器

[INPUT]: 依赖非敏感 config.json/config.example.json 与环境变量凭据
[OUTPUT]: 对外提供 load_config(), get_api_key(), get_sending_config(), get_competitors(), write_output()
[POS]: scripts/ 的基础设施，被所有其他脚本依赖
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─────────────────────────────────────────────
# 配置文件路径解析
# ─────────────────────────────────────────────

def _find_skill_root():
    """向上查找包含 SKILL.md 的目录作为 skill root"""
    current = Path(__file__).resolve().parent
    for _ in range(5):
        if (current / "SKILL.md").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


SKILL_ROOT = _find_skill_root()


def load_config():
    """加载 config.json，不存在则尝试 config.example.json"""
    config_path = SKILL_ROOT / "config.json"
    example_path = SKILL_ROOT / "config.example.json"

    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)

    if example_path.exists():
        print("  ⚠️  No config.json found. Using non-secret defaults from config.example.json")
        with open(example_path) as f:
            return json.load(f)

    print("  ❌ No config.json or config.example.json found.")
    sys.exit(1)


def get_api_key(_config, service):
    env_map = {
        "apollo": "APOLLO_API_KEY",
        "leadmagic": "LEADMAGIC_API_KEY",
        "instantly": "INSTANTLY_API_KEY",
        "brave": "BRAVE_API_KEY",
    }

    env_var = env_map.get(service, "")
    return os.environ.get(env_var, "")


def get_sending_config(config):
    """获取发送配置"""
    return config.get("sending", {})


def get_competitors(config):
    """获取竞对列表"""
    return config.get("competitors", [])


# ─────────────────────────────────────────────
# 统一输出格式
# ─────────────────────────────────────────────

def write_output(module, data, summary="", icp=None):
    """写入统一格式的 JSON 输出到 data/output/

    统一 schema:
    {
        "module": "instantly-audit",
        "timestamp": "2026-04-02T10:30:00Z",
        "icp": "saas-vp-marketing",
        "status": "success",
        "data": { ... },
        "summary": "一句话总结"
    }
    """
    output_dir = SKILL_ROOT / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"{today}-{module}.json"

    envelope = {
        "module": module,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "icp": icp,
        "status": "success",
        "data": data,
        "summary": summary,
    }

    with open(output_path, "w") as f:
        json.dump(envelope, f, indent=2, default=str)

    print(f"  💾 Output: {output_path}")
    return output_path


def load_icp_profile(icp_name):
    """加载指定 ICP 的 profile.json"""
    icp_path = SKILL_ROOT / "data" / "icps" / icp_name / "profile.json"
    if not icp_path.exists():
        print(f"  ❌ ICP not found: {icp_path}")
        print(f"     Run /30x-outreach {icp_name} to create it first.")
        return None

    with open(icp_path) as f:
        return json.load(f)


def load_business_profile():
    """加载业务 profile.json"""
    biz_path = SKILL_ROOT / "data" / "business" / "profile.json"
    if not biz_path.exists():
        return None

    with open(biz_path) as f:
        return json.load(f)
