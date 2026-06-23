# F0002-S0001 - Provider Adapter Contract

## Story Header

**Story ID:** F0002-S0001
**Feature:** F0002 - Managed Agent Orchestration
**Title:** Provider adapter contract
**Priority:** High
**Phase:** Future

## User Story

**As a** platform maintainer
**I want** a provider adapter contract that represents native exec, SDK, stream events, approvals, transcripts, and fallback behavior
**So that** future providers can be integrated without weakening the tmux-native behavior proven by F0001.

## Context & Background

Provider integration is dangerous when the contract only describes "send prompt, receive answer." Nebula's real product-build flow includes user feedback, tool approvals, gated stages, transcript recovery, and evidence artifacts. This story defines the adapter boundary before implementation choices are made.

## Acceptance Criteria

**Happy Path:**
- **Given** F0001 parity evidence exists
- **When** the adapter contract is reviewed
- **Then** it defines launch, input, stream, approval request, approval response, cancellation, transcript, gate event, validation event, and closeout event capabilities
- **Then** each provider capability is marked required, optional, unsupported, or fallback-to-tmux
- **Then** contract tests can verify a provider reports capability support before managed launch is available
- **Then** unsupported required capabilities deny managed launch and show tmux fallback guidance

**Alternative Flows / Edge Cases:**
- Provider lacks tool approval hooks; managed launch is denied and fallback guidance is shown.
- Provider supports streaming but not transcript export; managed launch is denied unless transcript is supplied by the Nebula event recorder.
- Provider capability probe times out; launch is blocked and audit evidence records timeout category.
- Provider reports a capability but contract test fails; managed mode remains unavailable for that provider.
- Local authorization policy denies managed mode; adapter details are visible but launch is blocked.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Adapter Health View | Run capability probe | Provider and mode selection | Writes capability report and audit entry | Provider mode selector reads the latest capability report | Local Operator, Reviewer, Architect |
| Provider Mode Selector | Inspect managed availability | No direct edit | No launch when required capability is missing | Availability remains blocked after reload until a passing probe exists | Local Operator; managed launch requires passing probe |

Required checks for mutation stories:
- [ ] Render-only behavior cannot satisfy capability probing.
- [ ] Capability report validates provider key, mode, required capability set, and fallback policy.
- [ ] Probe results have audit/timeline evidence.
- [ ] Tests prove unsupported required capabilities deny managed launch.

## Data Requirements

**Required Fields:**
- `provider_key`: Provider identifier.
- `provider_mode`: tmux-native, managed-exec, or managed-sdk.
- `capability_name`: Adapter capability being evaluated.
- `capability_status`: Required, Optional, Unsupported, or FallbackToTmux.
- `probe_result`: Pass, Fail, Timeout, or Skipped.
- `fallback_available`: Boolean.

**Optional Fields:**
- `provider_version`: Version observed during probe.
- `failure_reason`: Sanitized reason for failed capability.
- `contract_test_artifact`: Evidence path for probe output.

**Validation Rules:**
- Managed mode is unavailable when a required capability fails or is unsupported.
- Provider capability reports must not contain credentials.
- Fallback policy must be explicit for every unsupported capability.

## Role-Based Visibility

**Roles that can inspect or probe adapters:**
- Local Operator - Can run local probes.
- Reviewer - Can inspect reports and run validation probes.
- Architect - Can approve contract readiness.

**Data Visibility:**
- InternalOnly content: Provider versions, local command paths, detailed probe output.
- ExternalVisible content: Capability matrix and sanitized failure summary.

## Non-Functional Expectations

- Performance: Capability probe completes within provider-specific timeout limits.
- Security: Authorization policy blocks managed launch when provider auth boundaries are unknown.
- Reliability: Probe failures are deterministic enough for repeatable review evidence.

## Dependencies

**Depends On:**
- F0001 - Tmux-native cockpit behavior and evidence baseline.

**Related Stories:**
- F0002-S0005 - Migration uses adapter capability reports.

## Business Rules

1. Parity first: Adapter readiness is measured against F0001 behavior, not a thinner prompt-response abstraction.
2. Fallback explicit: Unsupported required capabilities must point to tmux-native fallback.
3. Capability before launch: Managed launch is disabled until capability probes pass.

## Out of Scope

- Implementing a full provider adapter.
- Removing tmux-native mode.
- Hosted provider credential storage.
- Remote multi-user adapter registry.

## UI/UX Notes

- Screens involved: Adapter health view, provider mode selector.
- Key interactions: Run probe, inspect capability matrix, follow fallback guidance.

## Questions & Assumptions

**Open Questions:**
- [ ] Should the adapter contract be language-neutral JSON schema, TypeScript types, Python dataclasses, or generated in multiple forms?

**Assumptions (to be validated):**
- F0001 will produce enough evidence to define the minimum required managed capabilities.
- Codex and Claude Code may need different adapter modes while sharing the same common event contract.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Permissions enforced for managed launch readiness
- [ ] Audit/timeline logged for capability probes and blocked launches
- [ ] Tests cover required capability pass, required capability fail, timeout, fallback, and denied managed launch
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
