# F0001 - Tmux-Native Agent Cockpit

**Status:** Planned
**Priority:** Critical
**Phase:** MVP

## Overview

F0001 delivers the first usable terminal UI for Nebula Agents by launching native Codex and Claude Code CLI sessions inside tmux. This preserves subscription-authenticated shells, native interactive prompts, gated approvals, and full terminal context while Nebula adds preflight checks, run tracking, evidence visibility, validation status, transcript capture, and recovery commands around the session.

## Documents

| Document | Purpose |
|----------|---------|
| [PRD.md](./PRD.md) | Full product requirements for the tmux-native cockpit |
| [STATUS.md](./STATUS.md) | Delivery checklist and signoff tracking |
| [GETTING-STARTED.md](./GETTING-STARTED.md) | Developer and agent setup guide |

## Stories

| ID | Title | Status |
|----|-------|--------|
| [F0001-S0001](./F0001-S0001-provider-auth-and-environment-preflight.md) | Provider auth and environment preflight | Not Started |
| [F0001-S0002](./F0001-S0002-tmux-session-launch-and-attach.md) | Tmux session launch and attach | Not Started |
| [F0001-S0003](./F0001-S0003-run-registry-and-evidence-watchers.md) | Run registry and evidence watchers | Not Started |
| [F0001-S0004](./F0001-S0004-gate-and-validator-dashboard.md) | Gate and validator dashboard | Not Started |
| [F0001-S0005](./F0001-S0005-native-session-transcript-and-recovery.md) | Native session transcript and recovery | Not Started |
| [F0001-S0006](./F0001-S0006-readonly-review-and-status-commands.md) | Read-only review and status commands | Not Started |

**Total Stories:** 6
**Completed:** 0 / 6

## Architecture Review

**Phase B status:** Not Started
**Execution Plan:** TBD

### Key Findings

- The first version must prefer `tmux + native CLI` over provider SDK calls because the primary product risk is loss of interactivity and subscription auth.
- The cockpit should observe and organize the native session; it should not reinterpret provider prompts or hide approval moments.
- F0002 can introduce provider adapters later, but F0001 remains the fallback behavior until managed orchestration proves parity.
