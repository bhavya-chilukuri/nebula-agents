# F0002 - Managed Agent Orchestration - Status

**Overall Status:** Draft
**Last Updated:** 2026-06-18

## Story Checklist

| Story | Title | Status |
|-------|-------|--------|
| F0002-S0001 | Provider adapter contract | [ ] Not Started |
| F0002-S0002 | Managed session thread continuity | [ ] Not Started |
| F0002-S0003 | Typed gate decision broker | [ ] Not Started |
| F0002-S0004 | Streaming event and approval bridge | [ ] Not Started |
| F0002-S0005 | Migration from tmux to managed orchestration | [ ] Not Started |

## Platform Progress

- [ ] Provider adapter contract drafted
- [ ] Capability probe model defined
- [ ] Managed session continuity model defined
- [ ] Typed event schema defined
- [ ] Approval broker defined
- [ ] F0001 parity checklist defined
- [ ] tmux fallback policy defined

## Terminal UI Progress

- [ ] Provider mode selector
- [ ] Managed run detail view
- [ ] Approval queue view
- [ ] Adapter health view
- [ ] Migration review view

## Cross-Cutting

- [ ] Story validator passes
- [ ] Tracker validator passes or documented bootstrap limitation is resolved
- [ ] Security review of provider auth and approval boundaries completed
- [ ] Architecture review of adapter boundary completed
- [ ] Migration evidence plan recorded

## Required Signoff Roles (Set in Planning)

| Role | Required | Why Required | Set By | Date |
|------|----------|--------------|--------|------|
| Quality Engineer | Yes | Validates managed-mode parity with F0001 and adapter contract behavior. | Architect | 2026-06-18 |
| Code Reviewer | Yes | Reviews provider adapter implementation and event handling. | Architect | 2026-06-18 |
| Security Reviewer | Yes | Reviews provider auth, approval routing, transcript, and secret boundaries. | Architect | 2026-06-18 |
| DevOps | No | Local-only future state unless a later feature adds hosted execution. | Architect | 2026-06-18 |
| Architect | Yes | Required for provider contract and migration approval. | Architect | 2026-06-18 |

## Story Signoff Provenance

Complete this before moving `Overall Status` to `Done` or `Archived`.

| Story | Role | Reviewer | Verdict | Evidence | Date | Notes |
|-------|------|----------|---------|----------|------|-------|
| F0002-S0001 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0002-S0001 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0002-S0001 | Security Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0002-S0001 | Architect | TBD | TBD | TBD | TBD | Pending implementation |

## Deferred Non-Blocking Follow-ups

| Follow-up | Why deferred | Tracking link | Owner |
|-----------|--------------|---------------|-------|

## Closeout Summary

| Field | Value |
|-------|-------|
| Implementation completed | TBD |
| Closeout review date | TBD |
| Total stories | 5 |
| Stories completed | 0 / 5 |
| Test count (unit + integration) | TBD |
| Defects found during review | TBD |
| Defects fixed before closeout | TBD |
| Residual risks | TBD |

## Tracker Sync Checklist

- [ ] `planning-mds/features/REGISTRY.md` status/path aligned
- [ ] `planning-mds/features/ROADMAP.md` section aligned
- [ ] `planning-mds/features/STORY-INDEX.md` regenerated or updated
- [ ] `planning-mds/BLUEPRINT.md` feature/story status links aligned
- [ ] Every required signoff role has story-level `PASS` entries with reviewer, date, and evidence
