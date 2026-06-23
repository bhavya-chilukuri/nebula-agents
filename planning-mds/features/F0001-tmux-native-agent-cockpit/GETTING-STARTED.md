# F0001 - Tmux-Native Agent Cockpit - Getting Started

## Prerequisites

- [ ] `tmux` installed and available on `PATH`.
- [ ] At least one supported provider CLI installed: `codex` or `claude`.
- [ ] Provider CLI authenticated in the shell where Nebula Agents is launched.
- [ ] Workspace root points at `/home/gajap/uSandbox/repos/nebula/nebula-agents` or an explicitly supplied product root.

## Services to Run

F0001 is local terminal tooling. No server is required for the MVP.

```bash
# Future commands should follow this shape once implemented:
nebula-agents doctor
nebula-agents tui
nebula-agents sessions
nebula-agents attach --run-id <RUN_ID>
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `NEBULA_AGENTS_PRODUCT_ROOT` | Product root used for planning docs and evidence paths. | Current working directory |
| `NEBULA_AGENTS_RUNTIME_DIR` | Local runtime state directory for session registry and transient files. | `.nebula-agents/runtime` |
| `NEBULA_AGENTS_PROVIDER` | Optional preferred provider key. | Auto-detect |

## Seed Data

No seed data is required. The first launch creates local run metadata for the selected feature or story.

## How to Verify

1. Run the preflight command and confirm `tmux` plus one provider CLI reports ready.
2. Launch a tmux-backed provider session for F0001.
3. Detach and reattach from the cockpit.
4. Trigger story and tracker validation from the cockpit.
5. Confirm run metadata, evidence path, and redacted transcript path are visible.

## Key Files

| Layer | Path | Purpose |
|-------|------|---------|
| Planning | `planning-mds/features/F0001-tmux-native-agent-cockpit/PRD.md` | Feature requirements |
| Planning | `planning-mds/features/F0001-tmux-native-agent-cockpit/F0001-S*.md` | Implementation stories |
| Prompts | `agents/templates/prompts/evidence-contract/` | Operator-friendly and automation-safe prompt contracts |
| Validation | `agents/product-manager/scripts/validate-stories.py` | Story completeness validation |
| Validation | `agents/product-manager/scripts/validate-trackers.py` | Tracker consistency validation |

## Dev User Credentials

Provider credentials are not managed by Nebula Agents. Use the local provider CLI login flow before launching the TUI. F0001 must not ask users to paste subscription credentials or API keys into Nebula-managed prompts.

## Notes

- A tmux launch should inherit the authenticated shell environment. If a provider prompts for login, the native provider CLI owns that interaction.
- Transcript capture must assume terminal output can contain sensitive data and must redact before writing review evidence.
- Do not split long-running feature builds into disconnected prompts for this MVP; the tmux session is the continuity boundary.
