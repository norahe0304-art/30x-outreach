"""
[INPUT]: 依赖 learning.ledger 的 append/load/verify 实现
[OUTPUT]: 对外暴露 append_record、load_records、verify_records、ledger_head
[POS]: learning 子包的稳定公共接口
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from .ledger import append_record, ledger_head, load_records, verify_records


__all__ = ["append_record", "ledger_head", "load_records", "verify_records"]
