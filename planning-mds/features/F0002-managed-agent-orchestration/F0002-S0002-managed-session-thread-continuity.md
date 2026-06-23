# F0002-S0002 - Managed Session Thread Continuity

## Story Header

**Story ID:** F0002-S0002
**Feature:** F0002 - Managed Agent Orchestration
**Title:** Managed session thread continuity
**Priority:** Critical
**Phase:** Future

## User Story

**As a** product build operator
**I want** managed sessions to preserve one coherent feature-build thread across planning, implementation, validation, and review
**So that** moving beyond tmux does not break the accumulated knowledge that makes the agent's engineering work good.

## Context & Background

The user's concern is correct: breaking a build into isolated prompt chunks can lose the knowledge gained in earlier stages. Managed orchestration must not mean stateless stage calls. It needs an explicit continuity model that carries prior artifacts, decisions, transcript summaries, validation output, and unresolved questions into later stages.

## Acceptance Criteria

**Happy Path:**
- **Given** a managed run starts from a feature and story set
- **When** the run advances from planning to implementation or validation
- **Then** the next stage receives a continuity package with feature PRD, story files, current decisions, gate history, evidence references, and transcript summary
- **Then** the provider sees prior unresolved questions and operator decisions before it performs the next stage
- **Then** the continuity package references source artifacts rather than only summarizing them
- **Then** each stage records the continuity package ID and audit evidence used for that stage

**Alternative Flows / Edge Cases:**
- Missing source artifact blocks stage advance and shows the missing path.
- Oversized continuity package is reduced by a documented summarization policy that preserves source references.
- Conflicting prior decisions block the run until the operator resolves the conflict.
- Provider context window limitations are recorded as a risk with visible fallback to tmux.
- Unauthorized local role cannot alter continuity package inputs.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Managed Run Detail | Advance stage | Stage target and optional operator note | Writes continuity package record and stage audit event | Reload shows continuity package ID and source artifact list | Local Operator; blocked when required artifacts are missing |
| Continuity Review | Resolve conflict | Conflict decision and reason | Appends decision to continuity audit trail | Later stages include the resolved decision reference | Local Operator or Architect depending on configured policy |

Required checks for mutation stories:
- [ ] Render-only behavior cannot satisfy stage continuity.
- [ ] Continuity package validates source artifacts, gate history, and operator decisions.
- [ ] Stage advance and conflict resolution have audit/timeline evidence.
- [ ] Tests prove later stages can recover continuity package references after restart.

## Data Requirements

**Required Fields:**
- `managed_session_id`: Logical managed run identity.
- `stage_id`: Current lifecycle stage.
- `continuity_package_id`: Identifier for context package.
- `source_artifacts`: Feature, story, evidence, transcript, and decision references.
- `gate_history`: Prior gate decisions.
- `operator_decisions`: User feedback and approvals that affect later stages.

**Optional Fields:**
- `summary_policy`: Policy used when context must be reduced.
- `context_window_risk`: Provider-specific limitation note.
- `conflict_records`: Unresolved or resolved continuity conflicts.

**Validation Rules:**
- Continuity package cannot omit feature PRD or active story files.
- Summaries must link back to source artifacts.
- Conflict resolution records are append-only.

## Role-Based Visibility

**Roles that can advance or resolve continuity:**
- Local Operator - Can advance stages and resolve ordinary continuity issues.
- Architect - Required for architecture-impacting conflict resolution when configured.
- Reviewer - Can inspect continuity packages read-only.

**Data Visibility:**
- InternalOnly content: Full local artifact paths and transcript summaries.
- ExternalVisible content: Sanitized continuity manifest and source reference list.

## Non-Functional Expectations

- Performance: Continuity package assembly completes within 5 seconds for normal feature sizes.
- Security: Authorization policy prevents read-only reviewers from altering continuity state.
- Reliability: A managed run can resume after process restart using stored continuity package references.

## Dependencies

**Depends On:**
- F0002-S0001 - Provider adapter contract must identify context and stage capabilities.
- F0001 - Baseline evidence defines expected continuity quality.

**Related Stories:**
- F0002-S0004 - Streaming event bridge records user feedback that becomes continuity input.
- F0002-S0005 - Migration compares continuity quality against tmux baseline.

## Business Rules

1. No stateless stage chunks: Managed orchestration must carry a deliberate continuity package into each stage.
2. Source references matter: Summaries without artifact references are not enough for review.
3. Fallback on context risk: If provider limits threaten continuity, managed mode must show tmux fallback.

## Out of Scope

- Infinite context retention.
- Automatic rewriting of PRDs or stories.
- Remote memory service.
- Replacing human gate decisions.

## UI/UX Notes

- Screens involved: Managed run detail, continuity review, conflict resolution prompt.
- Key interactions: Inspect continuity sources, advance stage, resolve conflict, choose fallback.

## Questions & Assumptions

**Open Questions:**
- [ ] What minimum source artifact set is required for each evidence-contract action: plan, feature, build, review, validate?

**Assumptions (to be validated):**
- F0001 transcripts and evidence will reveal the practical continuity artifacts needed for real builds.
- Provider context limits vary enough that continuity must be provider-aware.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Permissions enforced for stage advance and conflict resolution
- [ ] Audit/timeline logged for continuity package creation, stage advance, conflict resolution, and fallback
- [ ] Tests cover missing artifact, oversized package, conflict, unauthorized edit, restart recovery, and provider context risk
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
