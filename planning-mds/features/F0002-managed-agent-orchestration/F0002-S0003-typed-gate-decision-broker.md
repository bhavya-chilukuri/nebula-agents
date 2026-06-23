# F0002-S0003 - Typed Gate Decision Broker

## Story Header

**Story ID:** F0002-S0003
**Feature:** F0002 - Managed Agent Orchestration
**Title:** Typed gate decision broker
**Priority:** High
**Phase:** Future

## User Story

**As a** product owner
**I want** gate approvals, holds, recommendations, and evidence requirements represented as typed decision records
**So that** the TUI, CLI, and provider adapters use the same lifecycle rules.

## Context & Background

F0001 records gate decisions around a tmux session. F0002 needs those semantics to become provider-independent. A typed gate broker prevents each provider adapter or screen from inventing its own approval model, and it keeps managed orchestration aligned with the existing evidence contract.

## Acceptance Criteria

**Happy Path:**
- **Given** a managed run reaches a lifecycle gate
- **When** the gate broker evaluates the gate
- **Then** it returns required evidence, validator requirements, allowed decisions, required reviewer roles, and blocked reasons
- **When** an operator approves, holds, or records recommendations
- **Then** the broker writes a typed decision record with gate ID, decision, reviewer label, role, reason, evidence references, and timestamp
- **Then** provider adapters receive only the resulting allowed next action, not raw policy internals

**Alternative Flows / Edge Cases:**
- Missing evidence denies approval and records the blocked reason.
- Failed validator denies approval and links to the failing validation result.
- Unauthorized reviewer role is denied for approval and allowed to hold when policy permits.
- Duplicate approval requests are idempotent when the decision payload matches and rejected when it conflicts.
- Policy parse failure blocks the gate and records an audit event.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Gate Broker API | Evaluate gate | Gate ID and run ID | No decision mutation | Evaluation result can be recomputed from run state | TUI, CLI, adapter callers |
| TUI / CLI Gate Action | Approve, hold, or recommend | Decision, role, reviewer label, reason, evidence refs | Appends typed gate decision record | Decision appears after reload and adapter sees next allowed action | Local Operator, Reviewer, Architect per policy |

Required checks for mutation stories:
- [ ] Render-only behavior cannot satisfy gate decisions.
- [ ] Gate decisions validate role, evidence, validator status, and conflict state.
- [ ] Every decision has audit/timeline evidence.
- [ ] Tests prove unauthorized and blocked approvals do not advance the gate.

## Data Requirements

**Required Fields:**
- `gate_id`: Lifecycle gate identifier.
- `run_id`: Run being evaluated.
- `decision_id`: Unique decision record ID.
- `decision`: Approve, Hold, Recommend, or Blocked.
- `reviewer_role`: Local role used for policy evaluation.
- `reviewer_label`: Human-readable reviewer label.
- `evidence_refs`: Evidence paths or artifact IDs.
- `validator_refs`: Validation result references.
- `created_at`: ISO timestamp.

**Optional Fields:**
- `recommendations`: Non-blocking review notes.
- `supersedes_decision_id`: Prior decision replaced by a later explicit decision.
- `adapter_next_action`: Sanitized next action sent to provider adapter.

**Validation Rules:**
- Approval requires all required evidence and passing validators.
- Hold requires a reason.
- Decision records are append-only; supersession must reference the prior decision.

## Role-Based Visibility

**Roles that can decide gates:**
- Local Operator - Can approve or hold gates when policy permits.
- Reviewer - Can hold gates and record recommendations; approval depends on policy.
- Architect - Can approve architecture-sensitive gates when required.

**Data Visibility:**
- InternalOnly content: Policy internals, full local paths, reviewer labels.
- ExternalVisible content: Gate verdict, reason category, and sanitized evidence references.

## Non-Functional Expectations

- Performance: Gate evaluation returns within 500 ms for normal run state.
- Security: Authorization policy prevents role escalation and forged approval records.
- Reliability: Decision replay after restart produces the same current gate state.

## Dependencies

**Depends On:**
- F0001-S0004 - Gate semantics and validation states from tmux cockpit.
- F0002-S0001 - Adapter contract consumes broker output.

**Related Stories:**
- F0002-S0004 - Approval bridge routes provider requests and gate requests through visible user actions.

## Business Rules

1. One decision model: TUI, CLI, and adapters must share gate decision records.
2. Approval cannot bypass evidence: Missing evidence or failed validators block approval.
3. Provider adapters do not own lifecycle policy: They receive allowed actions from the broker.

## Out of Scope

- Remote identity provider integration.
- Pull request branch protection integration.
- Automatic gate approval.
- Retiring F0001 gate dashboard.

## UI/UX Notes

- Screens involved: Gate action prompt, managed run detail, approval queue.
- Key interactions: Evaluate gate, approve, hold, record recommendation, inspect blocked reason.

## Questions & Assumptions

**Open Questions:**
- [ ] Should role policy be a local config file for MVP or derived from planning feature status signoff roles?

**Assumptions (to be validated):**
- F0001 gate and validator dashboard can supply the initial evidence and decision vocabulary.
- Provider adapters can operate on a reduced next-action result without owning policy.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Permissions enforced for approval and hold semantics
- [ ] Audit/timeline logged for evaluations, approvals, holds, recommendations, policy errors, and blocked attempts
- [ ] Tests cover approval, hold, recommendation, missing evidence, failed validator, unauthorized role, duplicate decision, conflict, and replay
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
