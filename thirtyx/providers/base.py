"""
[INPUT]: 依赖标准库 dataclass 与 typing Protocol
[OUTPUT]: 对外提供 ProviderInfo、LeadSource、LeadVerifier、LeadDestination 契约
[POS]: providers 的稳定接口；具体 SaaS adapter 不得泄漏进核心 pipeline
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Protocol, Sequence


Lead = Dict[str, object]


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    capability: str
    description: str
    env_vars: Sequence[str]
    external_writes: bool = False


class LeadSource(Protocol):
    info: ProviderInfo

    def source(self, criteria: Dict[str, object], volume: int) -> List[Lead]:
        ...


class LeadVerifier(Protocol):
    info: ProviderInfo

    def verify(self, leads: Iterable[Lead]) -> List[Lead]:
        ...


class LeadDestination(Protocol):
    info: ProviderInfo

    def existing_emails(self) -> Iterable[str]:
        ...

    def upload(self, leads: Iterable[Lead], campaign_id: str) -> int:
        ...
