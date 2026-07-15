"""
[INPUT]: 依赖 campaign、evaluation 与 decision 字典
[OUTPUT]: 对外提供 terminal_text() sanitizer 与 render_terminal() 纯文本/ANSI proof
[POS]: rendering 的即时反馈入口，被 30x demo/evaluate/decide 消费
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import unicodedata


COLORS = {"green": "\033[32m", "yellow": "\033[33m", "red": "\033[31m", "cyan": "\033[36m", "bold": "\033[1m", "reset": "\033[0m"}


def terminal_text(value):
    return "".join(" " if unicodedata.category(character).startswith("C") else character for character in str(value)).strip()


def paint(text, color, enabled):
    return f"{COLORS[color]}{text}{COLORS['reset']}" if enabled else text


def score_bar(score):
    filled = round(score)
    return "█" * filled + "░" * (10 - filled)


def decision_color(decision):
    return {"SCALE": "green", "KILL": "red", "LEARN": "yellow", "COLLECT": "cyan"}.get(decision, "cyan")


def lens_lines(evaluation, color):
    return [
        f"  {score_bar(item['score'])} {item['score']:>4.1f}  {item['name'].replace('_', ' ')}"
        for item in evaluation["lenses"]
    ]


def render_terminal(campaign, evaluation, decision, color=True):
    verdict = paint(decision["decision"], decision_color(decision["decision"]), color)
    title = paint("30x OUTREACH · LEARNING REPORT", "bold", color)
    lines = [
        title, "═" * 58,
        f"Campaign   {terminal_text(campaign['campaign_id'])} · {terminal_text(campaign['sequence_version'])}",
        f"Audience   {terminal_text(campaign['audience'])}",
        f"Quality    {evaluation['score']:.1f}/100 · {terminal_text(evaluation['decision'])}",
        f"Decision   {verdict} · {terminal_text(decision['reason'])}", "",
        paint("TEN-LENS QUALITY GATE", "cyan", color),
        *lens_lines(evaluation, color), "",
        paint("LEARNING LOOP", "cyan", color),
        f"  Signal → Hypothesis → Sequence → Approval → {verdict} → Next wave",
        "═" * 58,
    ]
    return "\n".join(lines)
