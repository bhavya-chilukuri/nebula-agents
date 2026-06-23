# F0002 - Managed Agent Orchestration PRD

## Feature Header

**Feature ID:** F0002
**Feature Name:** Managed Agent Orchestration
**Priority:** High
**Phase:** Future Platform
**Status:** Draft

## Feature Statement

**As a** platform operator
**I want** Nebula Agents to manage provider sessions through explicit adapter contracts
**So that** mature orchestration can coordinate streaming output, approvals, gates, and evidence while preserving the interactive quality proven by F0001.

## Business Objective

- **Goal:** Move from tmux observation to managed orchestration only when provider adapters can preserve engineering quality.
- **Metric:** Managed runs meet or exceed F0001 behavior for context continuity, approval fidelity, gate validation, transcript recovery, and fallback support.
- **Baseline:** F0001 uses tmux to preserve native provider interactivity.
- **Target:** F0002 supports managed provider adapters with typed events and approvals while keeping tmux as fallback.

## Problem Statement

- **Current State:** SDK or exec-based orchestration can make provider runs easier to manage, but it can also drop native approval flows, user feedback loops, long-context continuity, and subscription-auth behavior.
- **Desired State:** Nebula introduces provider adapters only behind a contract that proves these behaviors explicitly.
- **Impact:** The product can mature beyond tmux without regressing into low-fidelity automation.

## Scope & Boundaries

**In Scope:**
- Provider adapter contract for exec, SDK, and future provider modes.
- Managed session model that preserves one logical thread across planning, build, validation, review, and gated approvals.
- Typed gate decision broker shared by TUI, CLI, and adapters.
- Streaming event bridge for provider output, tool approvals, user prompts, and lifecycle events.
- Side-by-side migration from F0001 tmux sessions to managed runs.

**Out of Scope:**
- Removing tmux fallback before parity evidence exists.
- Replacing product build prompts with unrelated simplified prompts.
- Multi-tenant hosted orchestration.
- Provider account management.
- Automatic approval of security-sensitive tool calls.

## Acceptance Criteria Overview

- [ ] A provider adapter contract exists for launch, stream, user input, approval requests, cancellation, transcript, and closeout events.
- [ ] Managed sessions preserve context across stages without stateless prompt fragmentation.
- [ ] Gate decisions use typed records shared across TUI and provider adapters.
- [ ] Streaming provider events can be rendered in the TUI and recorded as evidence.
- [ ] A migration plan lets an operator choose tmux or managed mode per run.
- [ ] Managed mode can fall back to tmux when provider parity is not available.

## UX / Screens

| Screen | Purpose | Key Actions |
|--------|---------|-------------|
| Provider Mode Selector | Choose tmux-native or managed provider mode. | Select mode, inspect parity status, launch. |
| Managed Run Detail | Show provider stream, prompts, approvals, gates, and evidence. | Send user feedback, approve provider requests, run validators. |
| Adapter Health | Show provider capability matrix. | Inspect supported features, run adapter tests. |
| Migration Review | Compare tmux and managed run evidence. | Accept parity, hold migration, keep fallback. |

**Key Workflows:**
1. Capability probe - adapter reports supported launch, stream, approval, transcript, and auth behaviors.
2. Managed run - operator launches a provider through the adapter and watches typed stream events.
3. Gate decision - operator approves or holds lifecycle gates through a shared broker.
4. Migration review - team compares managed evidence with F0001 evidence before promoting managed mode.

## Screen Layouts (ASCII)

### Managed Run Detail - Desktop

```text
+------------------------------------------------------------------+
| F0002 Managed Run                    Mode: managed  Fallback: on |
+---------------------------+--------------------------------------+
| Provider Stream           | Gate / Approval Queue                |
| event: assistant_output   | G3: Validation required              |
| event: tool_approval      | Provider tool request: pending       |
| event: user_prompt        | [Approve] [Deny] [Ask]               |
+---------------------------+--------------------------------------+
| Evidence: runs/...        | Context continuity: pass             |
+------------------------------------------------------------------+
```

### Provider Mode Selector - Narrow

```text
+------------------------------+
| Provider: Codex              |
| tmux-native: ready           |
| managed: partial             |
| Missing: tool approval hook  |
| [Launch tmux] [Launch managed disabled] |
+------------------------------+
```

## Data Requirements

**Core Records:**
- `provider_mode`: tmux-native, managed-exec, managed-sdk, or unavailable.
- `adapter_capabilities`: Supported event and control surfaces.
- `managed_session_id`: Logical managed run identity.
- `context_snapshot_refs`: References to prior artifacts and summaries loaded into the session.
- `stream_events`: Typed provider and orchestration events.
- `approval_requests`: Provider or lifecycle approvals awaiting user action.
- `fallback_run_id`: F0001 run ID used when managed mode falls back.

**Validation Rules:**
- Managed mode cannot be marked ready unless required capability probes pass.
- Context snapshots must reference source artifacts and generation timestamps.
- Approval decisions must be append-only and linked to the triggering request.

## Role-Based Access

| Role | Access Level | Notes |
|------|--------------|-------|
| Local Operator | Launch managed runs, respond to prompts, approve provider requests, approve gates | Same local-shell trust boundary as F0001 unless a future remote mode is designed. |
| Reviewer | Inspect managed run evidence and parity reports | Can hold migration until parity evidence is complete. |
| Architect | Approve provider contract and migration thresholds | Required for managed-mode promotion. |

## Success Criteria

- Managed mode can run at least one product-build flow with no loss of user feedback or gate approval fidelity.
- Adapter contract tests identify unsupported provider capabilities before launch.
- Operators can fall back to F0001 tmux mode without losing planning state.
- Closeout evidence demonstrates parity for interactivity, context continuity, validation, and recovery.

## Risks & Assumptions

- Risk: Provider SDKs do not expose all native interactive events. Mitigation: keep tmux fallback and capability gating.
- Risk: Context continuity degrades when managed orchestration summarizes too aggressively. Mitigation: require source artifact references and continuity checks.
- Risk: Approval routing becomes confusing. Mitigation: typed approval records with clear origin and allowed responses.
- Assumption: F0001 produces enough run/evidence metadata to guide migration requirements.

## Dependencies

- F0001 implemented and reviewed.
- Provider adapter feasibility research for Codex and Claude Code.
- Existing evidence-contract prompt behavior documented through F0001 runs.

## Related Stories

- [F0002-S0001](./F0002-S0001-provider-adapter-contract.md) - Provider adapter contract
- [F0002-S0002](./F0002-S0002-managed-session-thread-continuity.md) - Managed session thread continuity
- [F0002-S0003](./F0002-S0003-typed-gate-decision-broker.md) - Typed gate decision broker
- [F0002-S0004](./F0002-S0004-streaming-event-and-approval-bridge.md) - Streaming event and approval bridge
- [F0002-S0005](./F0002-S0005-migration-from-tmux-to-managed-orchestration.md) - Migration from tmux to managed orchestration

## Rollout & Enablement

- Start as experimental mode behind a local feature flag.
- Require parity reports before managed mode becomes the default for any provider.
- Preserve `tmux-native` as an explicit launch mode until a future feature retires it with evidence.
