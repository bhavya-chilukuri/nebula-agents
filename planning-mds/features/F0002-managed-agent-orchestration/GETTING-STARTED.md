# F0002 - Managed Agent Orchestration - Getting Started

## Prerequisites

- [ ] F0001 implemented and validated.
- [ ] F0001 run evidence available for at least one Codex and/or Claude Code terminal session.
- [ ] Provider capability research documented for any managed provider mode under consideration.
- [ ] Security review expectations agreed before provider auth or approval handling is implemented.

## Services to Run

F0002 is not the first build target. Early work should run in local experimental mode only.

```bash
# Future commands should follow this shape once F0001 exists:
nebula-agents providers doctor
nebula-agents tui --mode managed --provider codex
nebula-agents migration compare --baseline-run <F0001_RUN_ID> --managed-run <F0002_RUN_ID>
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `NEBULA_AGENTS_PROVIDER_MODE` | Selects `tmux-native`, `managed-exec`, or `managed-sdk`. | `tmux-native` |
| `NEBULA_AGENTS_MANAGED_EXPERIMENTAL` | Enables future managed mode during development. | `false` |
| `NEBULA_AGENTS_REQUIRE_TMUX_FALLBACK` | Blocks managed launch when tmux fallback is unavailable. | `true` |

## Seed Data

Use F0001 evidence packages as baseline data. F0002 should compare managed runs against real tmux-backed behavior, not only synthetic fixtures.

## How to Verify

1. Confirm F0001 launch, gate, validation, transcript, and recovery flows pass.
2. Run provider adapter capability probes.
3. Launch a managed experimental run only when required capability probes pass.
4. Compare managed output, approvals, context continuity, and evidence against F0001 baseline evidence.
5. Keep tmux fallback available for every provider until migration review approves parity.

## Key Files

| Layer | Path | Purpose |
|-------|------|---------|
| Planning | `planning-mds/features/F0002-managed-agent-orchestration/PRD.md` | Future managed orchestration requirements |
| Planning | `planning-mds/features/F0002-managed-agent-orchestration/F0002-S*.md` | Future implementation stories |
| Baseline | `planning-mds/features/F0001-tmux-native-agent-cockpit/` | Required tmux-native parity baseline |
| Prompts | `agents/templates/prompts/evidence-contract/` | Prompt contracts that managed mode must preserve |

## Dev User Credentials

Provider credentials remain outside Nebula-managed storage. Managed mode may request provider capabilities through local CLIs or SDKs, but it must not ask the user to paste subscription credentials into Nebula-owned prompts.

## Notes

- Treat SDK support as a capability, not a product goal by itself.
- Managed mode must prove it can carry user feedback and gate decisions without fragmenting the feature build context.
- F0001 remains the escape hatch while F0002 is experimental.
