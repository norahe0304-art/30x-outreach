"""
[INPUT]: 依赖 importlib.metadata entry points 与 ProviderInfo
[OUTPUT]: 对外提供 ProviderRegistry、default_registry()
[POS]: providers 的扩展发现层；第三方包通过 thirtyx.providers group 接入
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from importlib import metadata

from .base import ProviderInfo
from .builtins import BUILTIN_PROVIDERS


class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    def register(self, provider):
        info = provider if isinstance(provider, ProviderInfo) else getattr(provider, "info", None)
        if not isinstance(info, ProviderInfo):
            raise TypeError("provider must be ProviderInfo or expose ProviderInfo as .info")
        self._providers[(info.capability, info.name)] = provider
        return provider

    def discover(self):
        discovered = metadata.entry_points()
        entries = discovered.select(group="thirtyx.providers") if hasattr(discovered, "select") else discovered.get("thirtyx.providers", [])
        for entry in entries:
            self.register(entry.load()())
        return self

    def all(self):
        return tuple(self.info(key) for key in sorted(self._providers))

    def info(self, key):
        provider = self._providers[key]
        return provider if isinstance(provider, ProviderInfo) else provider.info

    def get(self, capability, name):
        provider = self._providers[(capability, name)]
        if isinstance(provider, ProviderInfo):
            raise LookupError(f"{capability}/{name} is metadata-only")
        return provider


def default_registry(discover=True):
    registry = ProviderRegistry()
    for info in BUILTIN_PROVIDERS:
        registry.register(info)
    return registry.discover() if discover else registry
