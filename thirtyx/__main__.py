"""
[INPUT]: 依赖 thirtyx.cli.main
[OUTPUT]: 支持 python -m thirtyx
[POS]: thirtyx package 的模块执行入口
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
