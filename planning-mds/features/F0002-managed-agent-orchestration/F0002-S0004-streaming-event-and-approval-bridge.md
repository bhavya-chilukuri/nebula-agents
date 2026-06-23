# F0002-S0004 - Streaming Event and Approval Bridge

## Story Header

**Story ID:** F0002-S0004
**Feature:** F0002 - Managed Agent Orchestration
**Title:** Streaming event and approval bridge
**Priority:** High
**Phase:** Future

## User Story

**As a** build operator
**I want** managed provider output, user prompts, tool approval requests, and lifecycle approvals rendered as typed TUI events
**So that** managed mode keeps the same interactive feedback loop users get from native terminal sessions.

## Context & Background

The screenshots and prompt examples show that successful runs are interactive. A managed provider surface must not hide user feedback, provider tool approvals, or gated decisions behind a background job. This story bridges provider streams and approval requests into visible TUI events with user-controlled responses.

## Acceptance Criteria

**Happy Path:**
- **Given** a managed provider emits output, user prompt, tool approval request, or lifecycle event
- **When** the event bridge receives it
- **Then** the TUI renders the event in order with origin, timestamp, event type, and allowed responses
- **When** the user responds to a prompt or approval request
- **Then** the response is recorded, routed to the correct provider or gate broker target, and appended to the audit timeline
- **Then** the transcript/evidence stream contains both the incoming event and the user's response

**Alternative Flows / Edge Cases:**
- Unknown event type is shown as unsupported and does not disappear from the stream.
- Provider disconnect blocks further responses and offers tmux fallback when available.
- Approval request expires; response controls are disabled and the expired state is recorded.
- Unauthorized local role cannot approve tool or lifecycle requests.
- Out-of-order events are rendered with sequence warnings and preserved for review.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Managed Run Detail | Respond to provider prompt | Response text or choice | Sends response to provider adapter and appends audit entry | Event stream replay shows prompt and response | Local Operator |
| Approval Queue | Approve, deny, or ask for details | Decision and optional reason | Routes decision to provider adapter or gate broker | Decision record survives reload and appears in evidence stream | Local Operator, Reviewer, Architect per policy |

Required checks for mutation stories:
- [ ] Render-only behavior cannot satisfy responses and approvals.
- [ ] Response routing validates request ID, role, event state, and allowed response.
- [ ] Incoming events and outgoing responses have audit/timeline evidence.
- [ ] Tests prove expired, unauthorized, unknown, and out-of-order events are handled.

## Data Requirements

**Required Fields:**
- `event_id`: Unique event identifier.
- `sequence`: Provider or bridge sequence number.
- `event_type`: Output, UserPrompt, ToolApproval, GateApproval, Error, or Unsupported.
- `origin`: Provider, Nebula, gate broker, validator, or operator.
- `allowed_responses`: Response choices or text permission.
- `request_status`: Pending, Responded, Expired, Denied, or Unsupported.
- `audit_ref`: Evidence reference for event and response.

**Optional Fields:**
- `response_payload`: Sanitized response content.
- `expires_at`: Expiration timestamp for pending approvals.
- `fallback_run_id`: tmux fallback when managed stream fails.

**Validation Rules:**
- Response is rejected when request is expired, already answered, or not allowed for role.
- Approval events must include origin and target.
- Event replay must preserve sequence and show warnings for gaps.

## Role-Based Visibility

**Roles that can respond:**
- Local Operator - Can respond to provider prompts and ordinary tool approvals.
- Reviewer - Can hold or request details when configured.
- Architect - Can decide architecture-sensitive lifecycle approvals.

**Data Visibility:**
- InternalOnly content: Full event stream, local evidence paths, provider request details.
- ExternalVisible content: Sanitized event summary and decision history.

## Non-Functional Expectations

- Performance: Stream events render within 250 ms of bridge receipt under normal local load.
- Security: Authorization policy applies before any response is routed to provider or gate broker.
- Reliability: Event replay after restart reconstructs pending and completed requests.

## Dependencies

**Depends On:**
- F0002-S0001 - Provider adapter contract defines stream and approval capabilities.
- F0002-S0003 - Gate broker handles lifecycle approval semantics.

**Related Stories:**
- F0002-S0002 - User feedback and decisions become continuity package input.

## Business Rules

1. Visible interaction: Managed mode must show prompts and approvals instead of burying them in logs.
2. User-controlled responses: No provider or lifecycle approval is answered automatically.
3. Event replay matters: Reviewers must be able to reconstruct what was asked and how the user responded.

## Out of Scope

- Voice or graphical notifications.
- Remote collaborative approval.
- Automatic response generation.
- Provider-specific UI skins.

## UI/UX Notes

- Screens involved: Managed run detail, approval queue, event stream.
- Key interactions: Read stream, answer prompt, approve, deny, ask for details, inspect event history.

## Questions & Assumptions

**Open Questions:**
- [ ] Should provider tool approvals and lifecycle gate approvals share one queue with different badges, or use separate panels?

**Assumptions (to be validated):**
- Provider adapters can expose enough event metadata to distinguish prompts, tool approvals, and plain output.
- Local TUI rendering can preserve event ordering without blocking provider execution.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Permissions enforced for prompt responses and approvals
- [ ] Audit/timeline logged for incoming events, outgoing responses, expired requests, denied requests, and fallback
- [ ] Tests cover stream ordering, response routing, unauthorized approval, expired request, unknown event, disconnect, and replay
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
