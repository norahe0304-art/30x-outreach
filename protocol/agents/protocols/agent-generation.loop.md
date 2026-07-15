<!--
[INPUT]: Depends on agent-onboarding.contract.md, protocol-consumption.contract.md, role-package.schema.md, capability-boundary.schema.md, run-state-ledger.protocol.md, geb-semantic-delta.md, the scaffold_consumer.py scaffolder, and the validators.
[OUTPUT]: Provides the executable loop that grows a conformant consumer agent from a real scenario, for any runtime.
[POS]: protocols generation loop; turns onboarding from a description into a runnable recipe. The protocol grows agents.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Agent Generation Loop

A consumer uses this protocol to grow its own agent from a real scenario, on
whatever runtime it picks. The protocol does not ship the answer; it ships the
shape (schema), the rules (gates), the hands (scaffolder), and the judge
(validators). Content is generated; structure is enforced.

This is the executable form of `agent-onboarding.contract.md`. Onboarding
describes the five steps; this loop runs them.

## Division of labor

```
deterministic (code, the hands)        |  generated (runtime, the judgment)
---------------------------------------+--------------------------------------
pin the protocol at a version          |  read the real scenario
correct paths + required schema fields |  fill tenant truth into the overlay
a green, minimal skeleton              |  write playbook steps + gates
the validator verdict                  |  iterate until green, then keep learning
```

Lock the mechanical, free the creative. This mirrors the whole protocol: schema
and gates are fixed; role / playbook / overlay / GEB-delta content is dynamic.

## The loop

```text
1. SCENARIO  collect the brief:
     domain, tenant, real systems (providers), approval surface,
     the role (use a reference role, fork one, or define your own),
     which playbooks the agent must run

2. SCAFFOLD  run the hands (deterministic):
     python3 scripts/scaffold_consumer.py \
       --domain <Domain> --tenant <Tenant> \
       --playbook <kebab> --dest <consumer-repo>
     default (no --role)         : generate your own role <domain>-operator (role-mode new)
     --role <id>                 : reuse a shipped reference role (role-mode reference)
     --role <id> --role-mode own : fork a reference role into your repo and adapt it
     --name <id>                 : override the instance id (default <tenant>-<domain>)
     -> pins the protocol under <dest>/protocol/
     -> emits a green, minimal overlay + mounted agent + workflow + entrypoint + state ledger
        (+ a local role, unless you referenced a shipped one)

3. GENERATE  fill the TODO markers from the scenario (any runtime):
     role*     -> identity, purpose, abstract surfaces, playbooks   (own/new only)
     overlay   -> source_of_truth, runtime_bindings, approval_surfaces, memory records
     mounted   -> playbook approval/readback lists, runtime_boundaries
     workflow  -> task_graph steps, capability_refs, apply_lab, evidence_packet
     state     -> reviewed tenant memory pointers only; no raw transcript, no secrets
     never bind a runtime; never store credentials; never edit protocol/

4. VALIDATE  run the judge:
     python3 protocol/scripts/validate_mounted_agents.py --root . --glob 'agents/*.agent.md'
     not green -> back to step 3. green -> the instance is well-formed.

5. DRY-RUN   warm up the runtime contract without side effects:
     python3 protocol/scripts/dry_run_agent.py \
       --root . --agent agents/<name>.agent.md --playbook <kebab>
     not green -> back to step 3. green -> runtime can parse the mounted contract.

6. RUN       point any runtime (Codex / Claude Code / Hermes / Browser / CLI) at
     agents/<name>.agent.md. The gates live in the playbook, so the runtime can
     be anything and still cannot bypass approval/evidence.

7. LEARN     after each real run, write a readback under agents/state/runs and
     route a GEB delta (geb-semantic-delta.md):
     tenant memory / workflow tail / skill candidate / protocol proposal,
     each carrying evidence + owner + review_after + contradiction_check.
     The agent keeps growing; the base role and protocol stay clean.
```

## Why this is safe to be dynamic

Generation is free, but every generated artifact passes the validator before it
runs, and every post-run change passes the GEB rails. A runtime can invent the
content; it cannot invent a way around the gates. That is the difference between
an adaptive agent and a hallucinating one.

## Roles are dynamic too

Marketing domains are unbounded, so the protocol does NOT decide which domains
exist. It ships the role *schema* and a small library of reference roles
(`agents/roles/`) as optional seeds. For your domain you may:

- `--role-mode reference` — mount a shipped reference role (reuse its wisdom);
- `--role-mode own` — fork a reference role into your repo and adapt it;
- `--role-mode new` — define your own role from the schema-shaped template.

Defining a new domain is a **consumer action, not a protocol change** — no PR, no
re-pin gate. The only thing the protocol grows centrally is the role *schema*. If
a role you wrote turns out broadly reusable, you may contribute it back to the
reference library, but that is optional, never required to ship.
