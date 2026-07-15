"""
[INPUT]: 依赖 providers.base 的 source、verifier、destination Protocol
[OUTPUT]: 对外提供 DemandPipeline 与去标识 PipelineResult
[POS]: thirtyx 的 provider-neutral orchestration；execute 是唯一 destination 写入门
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PipelineResult:
    sourced: int
    verified: int
    duplicates: int
    ready: int
    uploaded: int
    executed: bool

    def as_dict(self):
        return asdict(self)


def normalized_email(lead):
    return str(lead.get("email", "")).strip().lower()


def net_new_leads(leads, existing_emails):
    existing = {email.strip().lower() for email in existing_emails}
    seen = set()
    ready = []
    for lead in leads:
        email = normalized_email(lead)
        if email and email not in existing and email not in seen:
            seen.add(email)
            ready.append(lead)
    return ready


class DemandPipeline:
    def __init__(self, source, verifier, destination):
        self.source = source
        self.verifier = verifier
        self.destination = destination

    def run(self, criteria, volume, campaign_id, execute=False):
        sourced = self.source.source(criteria, volume)
        verified = self.verifier.verify(sourced)
        ready = net_new_leads(verified, self.destination.existing_emails())
        uploaded = self.destination.upload(ready, campaign_id) if execute and ready else 0
        return PipelineResult(
            sourced=len(sourced), verified=len(verified),
            duplicates=len(verified) - len(ready), ready=len(ready),
            uploaded=uploaded, executed=execute,
        )
