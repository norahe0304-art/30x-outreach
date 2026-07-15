"""
[INPUT]: 依赖 ProviderInfo 数据契约
[OUTPUT]: 对外提供 BUILTIN_PROVIDERS metadata
[POS]: providers 的内置能力目录，不包含凭据或网络副作用
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from .base import ProviderInfo


BUILTIN_PROVIDERS = (
    ProviderInfo("apollo", "source", "People and company search", ("APOLLO_API_KEY",)),
    ProviderInfo("leadmagic", "verify", "Work-email verification", ("LEADMAGIC_API_KEY",)),
    ProviderInfo("instantly", "destination", "Campaign dedupe and lead staging", ("INSTANTLY_API_KEY",), True),
    ProviderInfo("smtp", "send", "Approved plain-text email delivery", ("SENDER_EMAIL", "SMTP_PASSWORD"), True),
)
