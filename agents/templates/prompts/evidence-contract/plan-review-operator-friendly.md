This prompt encodes the plan-review action under the Feature Evidence Contract in `CONSUMER-CONTRACT.md` (effective `2026-05-19`). Plan review is a read-only post-plan readiness audit. It answers: `Is this plan ready to build?` It produces a base run evidence package per section 8 with `plan-review-report.md`; it does NOT write into any feature evidence package or repair planning artifacts.

REQUIRED INPUTS (you must set):
- `PLAN_SCOPE={feature | feature-set | project}`
- `TARGET={F#### | comma-separated F#### list | project}`

OPTIONAL INPUTS (defaults apply when omitted):
- `PRODUCT_ROOT=` - default: sister-repo resolved per `agents/docs/AGENT-USE.md` -> Session Setup; override only for non-standard layouts
- `DIFF_RANGE=` - optional SCM range when the review should focus on changed plan artifacts

AUTO-RESOLVED (do not set; SESSION_SETUP and the orchestrator compute these):
- `PLAN_REVIEW_RUN_ID` - `YYYY-MM-DD-{secrets.token_hex(4)}` generated once at session start
- `PLAN_REVIEW_RUN_FOLDER` - `{PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{PLAN_REVIEW_RUN_ID}`
- `FEATURE_SLUG` - kebab-case slug for `TARGET` from `REGISTRY.md` when `PLAN_SCOPE=feature`
- `FEATURE_PATH` - `{PRODUCT_ROOT}/planning-mds/features/{TARGET}-{FEATURE_SLUG}` when `PLAN_SCOPE=feature`

Echo the resolved absolute `{PRODUCT_ROOT}` path on your first turn before any shell command. Generate `PLAN_REVIEW_RUN_ID` once using the contract format `YYYY-MM-DD-[a-z0-9]{8}` with an 8-character suffix from cryptographic randomness. Do not use `uuid4`. Create `{PLAN_REVIEW_RUN_FOLDER}` and initialize the six section-8 base run files from templates: `README.md`, `action-context.md`, `artifact-trace.md`, `gate-decisions.md`, empty `commands.log`, and empty `lifecycle-gates.log`. Create `artifacts/` for command output capture.

Run `agents/actions/plan-review.md` with `PLAN_SCOPE`, `TARGET`, and `DIFF_RANGE` if provided.

Load context in this order: `agents/ROUTER.md` -> `agents/agent-map.yaml` -> `agents/docs/AGENT-USE.md` -> `agents/actions/plan-review.md` -> `agents/actions/plan.md` -> `agents/actions/feature.md` -> `agents/product-manager/SKILL.md` -> `agents/architect/SKILL.md` -> `agents/code-reviewer/SKILL.md`.

Read source artifacts directly. For feature scope, start with `{FEATURE_PATH}/**`, `REGISTRY.md`, `ROADMAP.md`, `BLUEPRINT.md`, and the knowledge-graph artifacts. Use `python3 {PRODUCT_ROOT}/scripts/kg/lookup.py {TARGET}` as a routing aid only; raw feature, ADR, API, schema, and policy artifacts win on conflict.

Don't write into any feature evidence package. Don't edit plan artifacts, trackers, stories, contracts, schemas, KG files, or architecture files. Don't approve from chat summaries, previous approval tokens, or generated checklists alone. Don't require `feature-assembly-plan.md` as a plan deliverable. Don't treat lookup/KG mappings as authoritative over raw artifacts. Don't downgrade missing build-critical detail to a low-severity note.

Keep ownership strict:
- Product Manager readiness review owns product, story, tracker, persona, UI/screen, and mutation-contract findings inside `plan-review-report.md`
- Architect readiness review owns architecture, API, schema, authorization, ADR, NFR, and KG-readiness findings inside `plan-review-report.md`
- Code Reviewer buildability challenge owns implementation-handoff, vertical-slice, testability, dependency, and risk-hotspot findings inside `plan-review-report.md`
- Reviewers produce findings only; owning lifecycle roles repair findings later through `plan.md` or targeted rework

Follow these gates exactly:

- `PR0 SCOPE LOCK` - record `PLAN_SCOPE`, `TARGET`, `DIFF_RANGE`, resolved feature paths, and review boundaries in `action-context.md`
- `PR1 PARALLEL READINESS REVIEW`:
  - Product Manager checks whether the requirements are specific, testable, traceable, and safe to hand to implementation without invented product rules
  - Architect checks whether implementation can start without new architecture, API, schema, workflow, authorization, ADR, NFR, or KG decisions
  - Code Reviewer challenges whether the plan is buildable as a vertical slice with clear role handoffs and test coverage paths
- `PR2 VALIDATOR PASS` - run applicable validator commands and append every command to `commands.log`:
  - `python3 agents/product-manager/scripts/validate-stories.py {FEATURE_PATH}` when feature scope is set
  - `python3 agents/product-manager/scripts/validate-trackers.py`
  - `python3 {PRODUCT_ROOT}/scripts/kg/validate.py`
  - `python3 {PRODUCT_ROOT}/scripts/kg/validate.py --check-drift`
  - `python3 agents/scripts/validate_templates.py`
- `PR3 SELF-REVIEW GATE` - each reviewer verifies findings cite exact files/sections, severities match build-readiness impact, skipped commands are justified, and no hidden fixes were made
- `PR4 READINESS GATE` - produce the readiness decision:
  - any critical finding -> `NOT READY`
  - no critical but any high finding -> `CONDITIONALLY READY`
  - no critical or high findings -> `READY`

Evidence outputs land in `{PLAN_REVIEW_RUN_FOLDER}`:
- section-8 base run files
- `plan-review-report.md`
- `artifacts/` command output captures when useful

`plan-review-report.md` must include: scope, run ID, date, review question, decision, rationale, next action, findings by severity, Product Readiness, Architecture Readiness, Buildability Challenge, Validation Evidence, and Artifact Trace.

Stop immediately if the target plan scope cannot be identified, required raw artifacts are missing and cannot be located, lookup returns only ambiguous or low-confidence matches for the declared target, a validator failure blocks evidence-based readiness, or reviewers cannot cite concrete files/sections for the readiness decision.

Close the run when `plan-review-report.md` is complete, `README.md` summarizes the readiness decision and open follow-ups, `gate-decisions.md` records PR0 through PR4, every applicable validator result is recorded, and no product or feature artifacts were edited by this review action.

Resolve conflicts like this:
- Raw artifact vs KG mapping -> raw wins; record KG drift as a finding
- PM and Architect readiness findings disagree -> record both and escalate at PR4
- Prior plan approval says ready but current artifacts have critical/high gaps -> current artifacts win
- Missing build-critical detail with no owner -> `NOT READY`
