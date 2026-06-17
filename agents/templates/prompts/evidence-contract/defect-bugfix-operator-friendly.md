This prompt encodes an ad hoc defect/bugfix run under the base run evidence profile in the Feature Evidence Contract in `CONSUMER-CONTRACT.md` (effective `2026-05-19`). Defect runs are outside the feature completion profile by default: they may change code, docs, tests, or planning notes, but they do NOT create feature evidence, do NOT satisfy completed-feature closeout requirements, and do NOT write `latest-run.json` unless explicitly promoted to a formal feature/build run.

REQUIRED INPUTS (you must set):
- `DEFECT_SUMMARY=` — short description of the bug or failure being chased
- `OBSERVED_BEHAVIOR=` — what is currently happening
- `EXPECTED_BEHAVIOR=` — what should happen instead

OPTIONAL INPUTS (defaults apply when omitted):
- `REPRO_STEPS=` — steps, URL/route, account/role, data fixture, or command that reproduces the bug
- `AFFECTED_PATHS=[path, path, ...]` — suspected code/docs/planning areas; empty means discover during triage
- `AGENT_ROLES=[architect, frontend-developer]` — default: `architect,frontend-developer`; add `product-manager`, `backend-developer`, `quality-engineer`, or `security-reviewer` only when relevant
- `FEATURE_REFS=[F####, F####, ...]` — optional read-only context references; does NOT make this feature-scoped evidence
- `ALLOW_FEATURE_PROPOSAL={false | true}` — default: `false`; when `true`, Product Manager may recommend a lightweight feature but must stop for approval before creating one
- `PRODUCT_ROOT=` — default: sister-repo resolved per `agents/docs/AGENT-USE.md` -> Session Setup; override only for non-standard layouts

AUTO-RESOLVED (do not set; SESSION_SETUP and the orchestrator compute these):
- `DEFECT_RUN_ID` — `YYYY-MM-DD-{secrets.token_hex(4)}` generated once at session start
- `DEFECT_RUN_FOLDER` — `{PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{DEFECT_RUN_ID}`
- `FEATURE_REF_PATHS` — feature paths resolved from `REGISTRY.md` only when `FEATURE_REFS` is set

Echo the resolved absolute `{PRODUCT_ROOT}` path and generated `{DEFECT_RUN_ID}` on your first turn before any shell command.

Generate `{DEFECT_RUN_ID}` once at session start using the contract format `YYYY-MM-DD-[a-z0-9]{8}` (suffix from `python3 -c "import secrets; print(secrets.token_hex(4))"`). Do not use `uuid4`. Do not regenerate `{DEFECT_RUN_ID}` after the session starts. Pass the same `{DEFECT_RUN_ID}` and `{DEFECT_RUN_FOLDER}` to every activated agent.

Create `{DEFECT_RUN_FOLDER}` at session start and initialize the six §8 base run files from templates: `README.md`, `action-context.md`, `artifact-trace.md`, `gate-decisions.md`, an empty `commands.log` (JSONL), and an empty `lifecycle-gates.log`. Create `artifacts/` for logs, screenshots, diffs, traces, and test output captures.

Record the defect scope in `{DEFECT_RUN_FOLDER}/action-context.md` before implementation: `DEFECT_SUMMARY`, `OBSERVED_BEHAVIOR`, `EXPECTED_BEHAVIOR`, `REPRO_STEPS`, `AFFECTED_PATHS`, `AGENT_ROLES`, `FEATURE_REFS`, `ALLOW_FEATURE_PROPOSAL`, and `Lifecycle Authority = none`.

Load context in this order: `agents/ROUTER.md` -> `agents/agent-map.yaml` -> `agents/docs/AGENT-USE.md` -> role skills for each entry in `AGENT_ROLES`. For `FEATURE_REFS`, load each referenced feature's `README.md`, `PRD.md`, `feature-assembly-plan.md`, and `STATUS.md` as read-only context; if archived, also load its approved `pm-closeout.md` when available.

Don't create or modify `planning-mds/features/*` unless the operator explicitly promotes this run to formal feature work after a Product Manager recommendation. Don't write into `####-*/`. Don't write `evidence-manifest.json`, `latest-run.json`, role signoff ledgers, or feature closeout artifacts. Don't treat this defect run as completed-feature evidence. Don't generate a second run ID for another activated agent. Don't hide failed commands; record them and use them as evidence.

Append every shell command to `{DEFECT_RUN_FOLDER}/commands.log` as JSON Lines per the §13 schema (`schema_version`, `timestamp` with timezone, `cwd`, `command`, `exit_code`, `artifacts[]`, `redactions[]`). Append validation milestones to `{DEFECT_RUN_FOLDER}/lifecycle-gates.log`; this file is a run audit log, not feature-stage validation.

Keep ownership strict:
- Product Manager, when activated, owns `{DEFECT_RUN_FOLDER}/bugfix-brief.md` with impact, affected users, acceptance checks, non-goals, and feature-promotion recommendation when needed. Product Manager must not create a feature unless the operator approves promotion.
- Architect owns `{DEFECT_RUN_FOLDER}/architect-analysis.md` with root-cause analysis, ownership boundary, design constraints, fix strategy, and risk assessment.
- Frontend Developer owns `{DEFECT_RUN_FOLDER}/frontend-fix-report.md` for UI/client changes, route-level behavior, state/data-flow fixes, screenshots when useful, and frontend test evidence.
- Backend Developer, when activated, owns `{DEFECT_RUN_FOLDER}/backend-fix-report.md` for API/domain/data changes and backend test evidence.
- Quality Engineer, when activated, owns `{DEFECT_RUN_FOLDER}/quality-report.md` with reproduction confirmation, regression tests, and validation matrix.
- Security Reviewer, when activated, owns `{DEFECT_RUN_FOLDER}/security-review-report.md` for auth/authz, data exposure, injection, secrets/config, and audit/logging implications.

Follow these gates exactly:
- `D0 DEFECT SCOPE LOCK` — confirm the bug statement, reproduction information, affected paths if known, active roles, and whether feature proposal is allowed; record the row in `gate-decisions.md`
- `D1 REPRODUCTION AND TRIAGE` — reproduce the bug or explain why it cannot be reproduced; capture relevant logs/screenshots/test failures under `artifacts/`; record initial findings in `artifact-trace.md`
- `D2 ROOT CAUSE AND FIX PLAN` — Architect identifies the root cause and smallest correct fix; Product Manager, when activated, confirms acceptance checks and non-goals; if the issue needs durable product tracking, write `feature-recommendation.md` and stop for approval when `ALLOW_FEATURE_PROPOSAL=true`, otherwise record a follow-up
- `D3 IMPLEMENTATION` — implement the smallest correct code/docs/planning fix within the defect scope; update or add focused regression tests where practical
- `D4 VALIDATION` — run the narrowest meaningful tests first, then broader validation only when blast radius requires it; record commands, exit codes, and artifacts
- `D5 REVIEW AND CLOSEOUT` — each activated role writes its report, `README.md` summarizes root cause/fix/validation/open follow-ups, and `gate-decisions.md` records the final defect-run verdict

If the operator approves promotion to formal feature work, stop this defect run cleanly first: record the promotion decision in `gate-decisions.md`, write `{DEFECT_RUN_FOLDER}/feature-recommendation.md`, and do not continue editing as a defect run. The next session must use the formal `plan`, `feature`, or `build` evidence contract with its own feature-scoped run ID and evidence package.

Evidence outputs land only in `{DEFECT_RUN_FOLDER}` plus the actual code/docs/planning files changed by the fix. `README.md` should include `Run Summary`, `Status`, `Evidence Index`, `Validation Summary`, and `Open Follow-ups`. `artifact-trace.md` should list artifacts read, artifacts created or updated, generated evidence, external/global evidence references, and omissions/waivers.

Stop immediately if the bug requires a new product capability rather than a defect fix and the operator has not approved feature promotion, if reproduction requires credentials/data/environment access that is unavailable, if a required validator or test fails for reasons unrelated to the fix after one repair cycle, if the fix would cross a security/privacy boundary without Security Reviewer involvement, or if `INSUFFICIENT_CONTEXT` occurs.

Close the run when the bug is either fixed and validated, explicitly not reproducible with evidence, or intentionally escalated. Confirm the six base run files are complete, role reports for activated agents are present, changed paths are listed in `artifact-trace.md`, and all commands needed to understand the decision are in `commands.log`.

Resolve conflicts like this:
- Architect recommends redesign but Frontend Developer can fix locally -> use the smallest correct local fix unless the redesign is needed to prevent recurrence; record the tradeoff in `architect-analysis.md`
- Product Manager says feature tracking is required but `ALLOW_FEATURE_PROPOSAL=false` -> stop and ask the operator whether to promote; do not create the feature
- Reproduction evidence disagrees with user report -> preserve both, state what was verified, and keep the run open only if there is a concrete next diagnostic step
- Tests pass but manual reproduction still fails -> manual reproduction wins; continue debugging or record the environment-specific blocker
- Feature references disagree with current code behavior -> current code and reproducible behavior are authoritative for the fix; feature docs become follow-up context unless the operator promotes the work
