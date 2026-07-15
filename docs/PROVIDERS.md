<!--
[INPUT]: 依赖 thirtyx.providers Protocol/registry 与 thirtyx.pipeline
[OUTPUT]: 对外提供第三方 provider 的最小实现、entry point 与注入方式
[POS]: docs 的扩展开发契约；示例必须与真实 registry API 同构
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Provider extensions

30x keeps vendor APIs outside the experiment core. A provider is a small object with a `ProviderInfo` descriptor and one capability method.

## Minimal source provider

```python
from thirtyx.providers import ProviderInfo


class CsvSource:
    info = ProviderInfo(
        name="csv",
        capability="source",
        description="Read leads from a reviewed CSV export",
        env_vars=(),
        external_writes=False,
    )

    def source(self, criteria, volume):
        return load_reviewed_rows(criteria["path"])[:volume]


def provider():
    return CsvSource()
```

Expose the factory from the provider package:

```toml
[project.entry-points."thirtyx.providers"]
csv = "my_thirtyx_provider:provider"
```

30x calls the entry point, validates `.info`, and registers the runnable instance.

```python
from thirtyx.providers import default_registry

source = default_registry().get("source", "csv")
```

## Capability contracts

- `LeadSource.source(criteria, volume)` returns lead dictionaries.
- `LeadVerifier.verify(leads)` returns only reviewed or verified lead dictionaries.
- `LeadDestination.existing_emails()` supports dedupe.
- `LeadDestination.upload(leads, campaign_id)` is the external write boundary.

Pass the implementations to `DemandPipeline`. The pipeline never calls `upload` unless `execute=True`.

## Provider checklist

- Put secrets in environment variables named by `ProviderInfo.env_vars`.
- Set `external_writes=True` for every destination or sender.
- Make reads idempotent and writes explicit.
- Return structured errors; never silently downgrade verification.
- Add an offline fake and prove preview causes zero writes.
- Do not store recipient PII in the learning ledger or public artifacts.

Built-in entries currently describe the credential and write surfaces of the legacy Apollo, LeadMagic, Instantly, and SMTP integrations. Promoting each into a standalone runnable adapter is tracked in the roadmap.
