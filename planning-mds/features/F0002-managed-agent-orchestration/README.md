# F0002 - Managed Agent Orchestration

**Status:** Planned
**Priority:** High
**Phase:** Future Platform

## Overview

F0002 defines the future state for Nebula Agents after the tmux-native cockpit proves the operating model. It introduces provider adapter contracts, managed session continuity, typed gate decisions, streaming event bridges, and a migration path from tmux-backed runs to managed orchestration without losing the interactive engineering quality established in F0001.

## Documents

| Document | Purpose |
|----------|---------|
| [PRD.md](./PRD.md) | Full product requirements for managed orchestration |
| [STATUS.md](./STATUS.md) | Delivery checklist and signoff tracking |
| [GETTING-STARTED.md](./GETTING-STARTED.md) | Future developer and agent setup guide |

## Stories

| ID | Title | Status |
|----|-------|--------|
| [F0002-S0001](./F0002-S0001-provider-adapter-contract.md) | Provider adapter contract | Not Started |
| [F0002-S0002](./F0002-S0002-managed-session-thread-continuity.md) | Managed session thread continuity | Not Started |
| [F0002-S0003](./F0002-S0003-typed-gate-decision-broker.md) | Typed gate decision broker | Not Started |
| [F0002-S0004](./F0002-S0004-streaming-event-and-approval-bridge.md) | Streaming event and approval bridge | Not Started |
| [F0002-S0005](./F0002-S0005-migration-from-tmux-to-managed-orchestration.md) | Migration from tmux to managed orchestration | Not Started |

**Total Stories:** 5
**Completed:** 0 / 5

## Architecture Review

**Phase B status:** Not Started
**Execution Plan:** TBD

### Key Findings

- F0002 must be treated as a maturity step, not the first build target.
- Provider adapters must prove parity with F0001 for user feedback, tool approvals, gate decisions, context continuity, transcripts, and recovery.
- tmux fallback remains required until closeout evidence proves managed orchestration can preserve the same quality bar.
