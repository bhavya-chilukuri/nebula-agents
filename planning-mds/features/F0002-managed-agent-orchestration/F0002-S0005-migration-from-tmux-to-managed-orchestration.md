# F0002-S0005 - Migration from Tmux to Managed Orchestration

## Story Header

**Story ID:** F0002-S0005
**Feature:** F0002 - Managed Agent Orchestration
**Title:** Migration from tmux to managed orchestration
**Priority:** Medium
**Phase:** Future

## User Story

**As a** product owner
**I want** a controlled upgrade path from tmux-native runs to managed provider orchestration
**So that** the team can improve Nebula Agents without losing the interactive quality and recovery guarantees established in F0001.

## Context & Background

The safest path is not to declare tmux temporary and remove it early. F0001 should become the baseline that managed mode must beat. Migration needs explicit parity checks, operator choice, fallback, and closeout evidence before managed mode becomes default.

## Acceptance Criteria

**Happy Path:**
- **Given** F0001 has completed evidence for a representative provider run
- **When** the operator opens migration review
- **Then** the review compares tmux-native and managed mode across auth reuse, prompt interactivity, tool approvals, gate decisions, validation, transcript, recovery, and context continuity
- **When** all required parity checks pass
- **Then** managed mode can be marked eligible for that provider while tmux fallback remains available
- **Then** the migration decision is recorded with reviewer roles, evidence references, and residual risks

**Alternative Flows / Edge Cases:**
- Missing F0001 baseline evidence blocks managed eligibility.
- Any failed parity check blocks default managed mode and recommends tmux fallback.
- Provider-specific parity passes for one provider but not another; eligibility is provider-scoped.
- Reviewer holds migration with recommendations; managed mode remains experimental.
- Unauthorized local role cannot mark managed mode eligible.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Migration Review | Compare baseline and managed run | Baseline run, managed run, provider, reviewer notes | Writes parity report and migration decision | Provider mode selector reads eligibility after reload | Product Owner, Architect, Quality Engineer |
| Provider Mode Selector | Choose launch mode | Provider mode selection | Launches selected eligible mode; tmux fallback remains selectable | Selection is recorded in run metadata | Local Operator; managed default requires eligibility |

Required checks for mutation stories:
- [ ] Render-only behavior cannot satisfy migration eligibility.
- [ ] Migration decision validates baseline evidence, managed evidence, reviewer role, and provider scope.
- [ ] Migration decision has audit/timeline evidence.
- [ ] Tests prove failed parity keeps managed mode experimental and fallback available.

## Data Requirements

**Required Fields:**
- `provider_key`: Provider under migration review.
- `baseline_run_id`: F0001 tmux-native run.
- `managed_run_id`: F0002 managed run.
- `parity_check_id`: Individual parity criterion.
- `parity_status`: Pass, Fail, Blocked, or NotApplicable.
- `migration_decision`: Experimental, Eligible, Held, or Rejected.
- `reviewer_roles`: Roles used for decision.
- `evidence_refs`: Baseline and managed evidence links.

**Optional Fields:**
- `residual_risks`: Accepted migration risks.
- `recommendations`: Follow-up work before promotion.
- `default_mode`: Provider default mode after eligibility.

**Validation Rules:**
- Eligibility is provider-scoped, not global.
- Managed default is denied when any required parity check fails.
- Tmux fallback cannot be disabled by this feature.

## Role-Based Visibility

**Roles that can decide migration eligibility:**
- Product Owner - Can accept or hold migration readiness.
- Architect - Required for provider contract and platform boundary approval.
- Quality Engineer - Required for parity evidence validation.
- Local Operator - Can choose mode when eligibility allows it.

**Data Visibility:**
- InternalOnly content: Full baseline and managed run evidence paths.
- ExternalVisible content: Provider eligibility status and sanitized parity summary.

## Non-Functional Expectations

- Performance: Migration review loads parity summaries within 2 seconds for normal evidence packages.
- Security: Authorization policy prevents unapproved roles from changing provider eligibility.
- Reliability: Provider mode selector never hides tmux fallback because of a failed managed capability.

## Dependencies

**Depends On:**
- F0001 completed evidence for tmux-native behavior.
- F0002-S0001 - Provider adapter contract.
- F0002-S0002 - Continuity model.
- F0002-S0003 - Gate broker.
- F0002-S0004 - Streaming and approval bridge.

**Related Stories:**
- F0001-S0005 - Transcript and recovery baseline.
- F0001-S0004 - Gate and validator baseline.

## Business Rules

1. F0001 is the baseline: Managed mode is promoted only by comparison to tmux-native evidence.
2. Provider-scoped eligibility: Passing for Codex does not imply passing for Claude Code, or the reverse.
3. Fallback remains: This feature cannot retire tmux-native mode.

## Out of Scope

- Removing tmux support.
- Hosted execution.
- Global provider default changes without review.
- Migrating historical evidence packages.

## UI/UX Notes

- Screens involved: Migration review, provider mode selector, parity report.
- Key interactions: Select baseline run, select managed run, compare checks, hold, mark eligible, launch fallback.

## Questions & Assumptions

**Open Questions:**
- [ ] What exact parity checklist should be required before managed mode becomes default for a provider?

**Assumptions (to be validated):**
- F0001 closeout evidence will include enough examples of approvals, user feedback, validation, transcript, and recovery.
- Operators may prefer tmux for some providers even after managed mode becomes eligible.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Permissions enforced for eligibility decisions and default mode selection
- [ ] Audit/timeline logged for parity report generation, holds, eligibility decisions, and launch-mode selection
- [ ] Tests cover missing baseline, failed parity, provider-scoped eligibility, unauthorized decision, fallback visibility, and reload
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
