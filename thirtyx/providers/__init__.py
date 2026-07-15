"""
[INPUT]: 依赖 providers.base 与 providers.registry
[OUTPUT]: 对外提供 ProviderInfo、Protocol 与 default_registry
[POS]: thirtyx.providers 的公共插件入口
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from .base import LeadDestination, LeadSource, LeadVerifier, ProviderInfo
from .registry import ProviderRegistry, default_registry

__all__ = ["LeadDestination", "LeadSource", "LeadVerifier", "ProviderInfo", "ProviderRegistry", "default_registry"]
