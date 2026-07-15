"""
[INPUT]: 依赖 rendering.html 与 rendering.terminal
[OUTPUT]: 对外提供 render_html、write_html、terminal_text、render_terminal
[POS]: thirtyx.rendering 的公共渲染入口
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from .html import render_html, write_html
from .terminal import render_terminal, terminal_text

__all__ = ["render_html", "render_terminal", "terminal_text", "write_html"]
