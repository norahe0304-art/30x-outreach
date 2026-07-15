"""
[INPUT]: 依赖 frozen campaign spec 与 Instantly campaign analytics 聚合导出
[OUTPUT]: 对外提供 observation_from_instantly() 的去标识 experiment observation
[POS]: thirtyx 的 provider result adapter；只转换聚合计数，不读取或保存 recipient PII
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from datetime import datetime, timezone


RATE_FIELDS = (
    ("human_reply_rate", ("reply_count_unique", "reply_count")),
    ("automatic_reply_rate", ("reply_count_automatic_unique", "reply_count_automatic")),
    ("positive_reply_rate", ("positive_reply_count", "total_interested")),
    ("bounce_rate", ("bounced_count",)),
    ("unsubscribe_rate", ("unsubscribed_count",)),
    ("meeting_booked_rate", ("total_meeting_booked",)),
    ("opportunity_rate", ("total_opportunities",)),
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def campaign_analytics(payload, campaign_id):
    rows = payload if isinstance(payload, list) else [payload]
    matches = [row for row in rows if isinstance(row, dict) and row.get("campaign_id") == campaign_id]
    if not matches:
        raise ValueError("Instantly analytics has no row for campaign_id")
    if len(matches) > 1:
        raise ValueError("Instantly analytics has duplicate rows for campaign_id")
    return matches[0]


def count(row, names):
    for name in names:
        if name not in row:
            continue
        value = row[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Instantly analytics {name} must be a non-negative number")
        return value
    return None


def observation_from_instantly(campaign, payload, observed_at=None):
    row = campaign_analytics(payload, campaign["campaign_id"])
    sample_size = count(row, ("new_leads_contacted_count", "contacted_count"))
    if not isinstance(sample_size, int) or isinstance(sample_size, bool) or sample_size < 1:
        raise ValueError("Instantly analytics needs a positive integer contacted count")
    metrics = {}
    for metric, fields in RATE_FIELDS:
        numerator = count(row, fields)
        if numerator is not None:
            metrics[metric] = numerator / sample_size
    emails_sent = count(row, ("emails_sent_count",))
    if emails_sent is not None:
        metrics["emails_per_lead"] = emails_sent / sample_size
    if not metrics:
        raise ValueError("Instantly analytics contains no supported aggregate metrics")
    return {
        "schema_version": "1.0",
        "campaign_id": campaign["campaign_id"],
        "sequence_version": campaign["sequence_version"],
        "observed_at": observed_at or utc_now(),
        "sample_size": sample_size,
        "metrics": metrics,
        "notes": "Imported from Instantly aggregate analytics; rates use new leads contacted as denominator.",
    }
