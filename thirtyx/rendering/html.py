"""
[INPUT]: 依赖去标识 campaign、evaluation 与 decision 字典
[OUTPUT]: 对外提供 render_html()、write_html() 单文件 proof artifact
[POS]: rendering 的可分享报告生成器；不加载外部脚本、字体或网络资源
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from html import escape
from pathlib import Path


STYLES = """
:root{--ink:#eaf0ff;--muted:#8c98b8;--panel:#11182a;--line:#26324d;--violet:#9b87f5;--cyan:#4fd1c5;--green:#68d391;--red:#fc8181;--yellow:#f6e05e}
*{box-sizing:border-box}body{margin:0;background:#080c16;color:var(--ink);font:15px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
.wrap{max-width:1100px;margin:auto;padding:48px 28px 72px}.eyebrow{color:var(--cyan);letter-spacing:.18em;text-transform:uppercase;font-size:12px}
h1{font:700 clamp(36px,6vw,72px)/1.02 ui-sans-serif,system-ui;margin:12px 0 16px;letter-spacing:-.045em}.lede{max-width:760px;color:var(--muted);font:18px/1.55 ui-sans-serif,system-ui}
.badges{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0 34px}.badge{border:1px solid var(--line);border-radius:999px;padding:7px 12px;color:var(--muted)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:linear-gradient(145deg,#121a2d,#0e1423);border:1px solid var(--line);border-radius:18px;padding:22px}
.hero{display:grid;grid-template-columns:220px 1fr;gap:28px;align-items:center;margin:20px 0 16px}.score{width:180px;height:180px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--green) calc(var(--score)*1%),#1a2237 0);position:relative}
.score:after{content:"";position:absolute;inset:12px;border-radius:50%;background:#0d1424}.score strong{z-index:1;font:700 44px ui-sans-serif,system-ui}.score small{display:block;color:var(--muted);font-size:11px;text-align:center}
.decision{font:800 48px ui-sans-serif,system-ui;letter-spacing:-.03em}.SCALE{color:var(--green)}.KILL{color:var(--red)}.LEARN{color:var(--yellow)}.COLLECT{color:var(--cyan)}
.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:16px 0 28px}.flow span{padding:13px 8px;text-align:center;border:1px solid var(--line);border-radius:10px;color:var(--muted);font-size:12px}.flow span:last-child{border-color:var(--violet);color:var(--ink)}
.lens{display:grid;grid-template-columns:180px 1fr 52px;gap:14px;align-items:center;margin:13px 0}.track{height:9px;background:#1a2237;border-radius:9px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,var(--violet),var(--cyan))}
.meta{color:var(--muted)}h2{font:700 22px ui-sans-serif,system-ui;margin:0 0 16px}.footer{margin-top:28px;color:var(--muted);font-size:12px}
@media(max-width:760px){.grid,.hero{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}.lens{grid-template-columns:130px 1fr 42px}.score{margin:auto}}
"""


def lens_markup(evaluation):
    rows = []
    for item in evaluation["lenses"]:
        name = escape(item["name"].replace("_", " "))
        rows.append(f'<div class="lens"><span>{name}</span><div class="track"><div class="fill" style="width:{item["score"]*10}%"></div></div><b>{item["score"]:.1f}</b></div>')
    return "".join(rows)


def render_html(campaign, evaluation, decision):
    title = escape(campaign["campaign_id"])
    audience = escape(campaign["audience"])
    hypothesis = escape(campaign["experiment"]["hypothesis"])
    verdict = escape(decision["decision"])
    reason = escape(decision["reason"])
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>30x · {title}</title><style>{STYLES}</style><body><main class="wrap">
<div class="eyebrow">30x Outreach · auditable demand experiments</div><h1>Every campaign should make the next one smarter.</h1><p class="lede">A proof artifact connecting verified signals, frozen hypotheses, deterministic quality, human approval, and the next growth decision.</p>
<div class="badges"><span class="badge">{title}</span><span class="badge">{escape(campaign['sequence_version'])}</span><span class="badge">DEMO DATA</span></div>
<section class="card hero"><div class="score" style="--score:{evaluation['score']}"><strong>{evaluation['score']:.0f}<small>QUALITY / 100</small></strong></div><div><div class="decision {verdict}">{verdict}</div><p class="meta">{reason}</p><p>{audience}</p></div></section>
<div class="flow"><span>VERIFIED SIGNAL</span><span>HYPOTHESIS</span><span>SEQUENCE</span><span>10-LENS GATE</span><span>HUMAN APPROVAL</span><span>{verdict}</span></div>
<div class="grid"><section class="card"><h2>Quality gate</h2>{lens_markup(evaluation)}</section><section class="card"><h2>Frozen experiment</h2><p class="meta">HYPOTHESIS</p><p>{hypothesis}</p><p class="meta">PRIMARY METRIC</p><p>{escape(decision['primary_metric'])}: {decision['primary_value']}</p><p class="meta">NEXT SYSTEM INPUT</p><p>{reason}</p></section></div>
<p class="footer">Generated locally by 30x. No external assets, trackers, credentials, or recipient PII.</p></main></body></html>'''


def write_html(path, campaign, evaluation, decision):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(campaign, evaluation, decision), encoding="utf-8")
    return output
