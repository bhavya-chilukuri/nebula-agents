# Feature Roadmap (Now / Next / Later)

**Last Reviewed:** 2026-06-18

## Purpose

This roadmap sequences Nebula Agents work so the team can validate one delivery step before starting the next. It is intentionally conservative: tmux-native session orchestration comes first because it preserves the current interactive quality of Codex and Claude Code. Managed SDK/provider orchestration comes later only after parity is proven.

## Update Rules

- Move a feature between `Now`, `Next`, `Later`, and `Completed` when its execution state changes.
- Keep links aligned with `REGISTRY.md`, `STORY-INDEX.md`, and `BLUEPRINT.md`.
- Do not place F0002 in `Now` until F0001 validates provider auth reuse, interactive approval preservation, gate visibility, transcript recovery, and validator integration.

## Now

| Feature | Status | Why Now | Validation Gate |
|---------|--------|---------|-----------------|
| [F0001 - Tmux-Native Agent Cockpit](./F0001-tmux-native-agent-cockpit/) | Planned | Establish the first usable terminal cockpit without losing native agent interactivity or subscription auth. | Operator can launch, attach, monitor, validate, and recover a native Codex or Claude Code session from the TUI. |

## Next

| Feature | Status | Why Next | Entry Criteria |
|---------|--------|----------|----------------|
| [F0002 - Managed Agent Orchestration](./F0002-managed-agent-orchestration/) | Planned | Add provider adapters and richer orchestration once tmux behavior is understood and testable. | F0001 is implemented, reviewed, and has evidence that native interactivity can be preserved or matched. |

## Later

| Feature | Status | Notes |
|---------|--------|-------|

## Completed

| Feature | Completed Date | Evidence |
|---------|----------------|----------|

## Notes

- F0001 is a subscription-first implementation path. It should call authenticated local CLIs, not API-key-only SDK flows.
- F0002 may support SDK and exec-based providers, but it must keep a tmux fallback until managed orchestration proves equivalent engineering quality.
