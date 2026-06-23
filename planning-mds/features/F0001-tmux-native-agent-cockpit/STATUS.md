# F0001 - Tmux-Native Agent Cockpit - Status

**Overall Status:** Draft
**Last Updated:** 2026-06-18

## Story Checklist

| Story | Title | Status |
|-------|-------|--------|
| F0001-S0001 | Provider auth and environment preflight | [ ] Not Started |
| F0001-S0002 | Tmux session launch and attach | [ ] Not Started |
| F0001-S0003 | Run registry and evidence watchers | [ ] Not Started |
| F0001-S0004 | Gate and validator dashboard | [ ] Not Started |
| F0001-S0005 | Native session transcript and recovery | [ ] Not Started |
| F0001-S0006 | Read-only review and status commands | [ ] Not Started |

## CLI / Core Progress

- [ ] Preflight command implemented
- [ ] Provider CLI discovery implemented
- [ ] Tmux session naming and launch implemented
- [ ] Run registry implemented
- [ ] Evidence watchers implemented
- [ ] Transcript capture and redaction implemented
- [ ] Recovery and attach commands implemented

## Terminal UI Progress

- [ ] Session list view
- [ ] Session detail view
- [ ] Gate status view
- [ ] Validator output view
- [ ] Keyboard navigation
- [ ] Terminal resize behavior verified

## Cross-Cutting

- [ ] Story validator passes
- [ ] Tracker validator passes or documented bootstrap limitation is resolved
- [ ] No provider auth secrets are persisted
- [ ] Transcript redaction test coverage added
- [ ] Runtime validation evidence recorded
- [ ] README and getting-started docs updated

## Required Signoff Roles (Set in Planning)

| Role | Required | Why Required | Set By | Date |
|------|----------|--------------|--------|------|
| Quality Engineer | Yes | Validates preflight, tmux launch, gate, transcript, and recovery behavior. | Architect | 2026-06-18 |
| Code Reviewer | Yes | Reviews CLI/TUI implementation quality and failure-mode handling. | Architect | 2026-06-18 |
| Security Reviewer | Yes | Reviews provider auth boundaries, transcript redaction, and secret handling. | Architect | 2026-06-18 |
| DevOps | No | Local-only MVP with no deployment surface planned. | Architect | 2026-06-18 |
| Architect | Yes | Confirms tmux-first boundary and F0002 migration assumptions. | Architect | 2026-06-18 |

## Story Signoff Provenance

Complete this before moving `Overall Status` to `Done` or `Archived`.

| Story | Role | Reviewer | Verdict | Evidence | Date | Notes |
|-------|------|----------|---------|----------|------|-------|
| F0001-S0001 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0001-S0001 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0001-S0001 | Security Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0001-S0001 | Architect | TBD | TBD | TBD | TBD | Pending implementation |

## Deferred Non-Blocking Follow-ups

| Follow-up | Why deferred | Tracking link | Owner |
|-----------|--------------|---------------|-------|

## Closeout Summary

| Field | Value |
|-------|-------|
| Implementation completed | TBD |
| Closeout review date | TBD |
| Total stories | 6 |
| Stories completed | 0 / 6 |
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
