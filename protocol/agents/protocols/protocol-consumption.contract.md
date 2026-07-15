<!--
[INPUT]: Depends on role-package.schema.md, agent-onboarding.contract.md, install-mount-lifecycle.protocol.md, and the scripts/ validators.
[OUTPUT]: Provides the contract for how an external repo pins, references, and validates this protocol to grow its own agent.
[POS]: protocols consumption boundary; turns the protocol from one local repo into a versioned spec any repo can read.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Protocol Consumption Contract

This protocol is a product other repos consume. A consumer reads the protocol,
fills in role + playbook + tenant truth for its real scenario, and points any
agent runtime at the result. This file defines how that consumption works so an
instance can live in a different repo and still validate.

The protocol ships only the invariants: **schema + gates + validators +
run-state rails + GEB learning rails**. role / playbook / overlay / readback /
GEB-delta *content* is generated per scenario by the consumer. Runtime is the
consumer's choice. Tenant instances do not live here.

## What the protocol ships (the invariant)

```
agents/protocols/   contracts + schemas (this layer)
agents/roles/       reference roles = optional seeds (use, fork, or replace) + schema proof
agents/templates/   stubs the generation loop stamps into a consumer instance
scripts/            validators + dry-run warm-up + scaffolder + skill builder + pre-commit hook
```

## What a consumer holds (the generated instance)

```
<consumer-repo>/
  protocol/                 pinned copy of this protocol at a version (see Pinning)
  agents/
    <tenant>.overlay.md     tenant truth; mounts_on a base role id
    <tenant>.agent.md       mounted agent: role + tenant_attachment + work_substrate + entrypoints
    workflows/*.workflow.md  playbook contracts (reference role/overlay by id)
    state/
      runs/*.readback.yaml   structured run readbacks
      deltas/*.yaml          verified learning deltas
      memory/tenant-memory.md reviewed tenant memory pointers
```

## Pinning

A consumer pins one protocol version. Two supported mechanisms:

```yaml
protocol_pin:
  name: adaptive-marketing-agent-os
  version: v0.3.10
  mechanism: vendored-copy        # or: git-submodule
  vendored_copy:
    path: protocol/               # protocol tree copied under here
    stamp: protocol/VERSION       # records name, version, source commit
    resync: "re-copy agents/{protocols,roles} + scripts at the new tag"
  git_submodule:
    path: protocol/
    url: https://github.com/norahe0304-art/adaptive-marketing-agent-os.git
    pinned_ref: v0.3.10           # checkout the tag commit, then `git add protocol`
```

`vendored-copy` is the default: self-contained, offline-verifiable, no submodule
ceremony. `git-submodule` is the stricter pin when the consumer wants the exact
commit tracked by git.

## Reference resolution

References are ordinary relative paths, resolved against the consumer repo root:

- **protocol-layer refs** point into the pinned copy: `protocol/agents/roles/...`,
  `protocol/agents/protocols/...`.
- **instance-layer refs** are consumer-local: `agents/<tenant>.overlay.md`,
  `agents/workflows/...`.
- **work_substrate / entrypoints** are consumer-local or absolute machine paths.
- **role / overlay inside a workflow** are referenced by **id**, not path, so
  workflows are path-portable and move between repos unchanged.

No URI scheme, no resolver: because the protocol is physically present at
`protocol/`, every path just resolves.

## Validation

The consumer runs the protocol's own validator against its repo:

```bash
python3 protocol/scripts/validate_mounted_agents.py \
  --root . \
  --glob 'agents/*.agent.md'
```

Green means: the mounted agent resolves its base role (in the pinned protocol),
its tenant attachment, its work substrate, its entrypoints, and every playbook
workflow contract — i.e. the instance is correctly assembled against the pinned
protocol. The protocol repo itself stays green with zero tenants: its mounted
glob is empty (valid for a spec repo) and the reference roles prove the schema.

The consumer can then warm up a runtime without side effects:

```bash
python3 protocol/scripts/dry_run_agent.py \
  --root . \
  --agent agents/<tenant>.agent.md \
  --playbook <playbook>
```

Green means the runtime can parse the mounted agent, resolve role/overlay/
workflow/state, inspect TODO debt, and emit a readback skeleton before touching
external systems.

## Lifecycle

```text
pin protocol@version
  -> generate overlay + mounted + workflows for the real scenario
  -> validate against the pinned protocol
  -> dry-run boot the mounted playbook
  -> point any runtime (Codex / Claude Code / Hermes / browser / local / MCP-backed) at <tenant>.agent.md
  -> run -> write readback under agents/state/runs -> report learning verdict -> route verified GEB delta
  -> bump protocol version when the spec evolves; re-pin and re-validate
```

## Rules

- A consumer never edits files under `protocol/`. Protocol changes happen in the
  protocol repo, get a new version, and reach the consumer through a re-pin.
- A consumer never copies tenant truth, credentials, or live mutation permission
  into `protocol/`.
- A consumer stores secret references only (`${ENV_NAME}`, `vault://...`,
  `1password://...`), never literal API keys, OAuth tokens, passwords, or
  private keys.
- A consumer stores durable learning as structured readbacks and reviewed
  deltas, not raw chat transcripts.
- Generated role/playbook/overlay/GEB content is free; the validator is the gate
  that keeps every generated artifact safe and composable.
- Bumping the protocol version is the only way new shared semantics (schema
  fields, capability profiles, approval states, GEB routes) reach consumers.
