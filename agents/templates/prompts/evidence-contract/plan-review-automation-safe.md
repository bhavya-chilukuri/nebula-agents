ACTION: agents/actions/plan-review.md
CONTRACT: Feature Evidence Contract in CONSUMER-CONTRACT.md (effective 2026-05-19)
CONTRACT SCOPE: Plan review is a read-only post-plan readiness audit. It answers "Is this plan ready to build?" and writes a base run evidence package with plan-review-report.md. It never writes into a feature evidence package and never repairs plan artifacts during review.

REQUIRED INPUTS (operator must set before SESSION_SETUP):
  PLAN_SCOPE:           {feature | feature-set | project}
  TARGET:               {F#### | comma-separated F#### list | project}

OPTIONAL INPUTS (defaults apply when omitted):
  PRODUCT_ROOT:         absolute product repo root             # default: sister-repo per agents/docs/AGENT-USE.md
  DIFF_RANGE:           SCM range for changed planning artifacts

AUTO-RESOLVED (do not set; SESSION_SETUP and the orchestrator compute these):
  PLAN_REVIEW_RUN_ID     = YYYY-MM-DD-{secrets.token_hex(4)} generated at SESSION_SETUP
  PLAN_REVIEW_RUN_FOLDER = {PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{PLAN_REVIEW_RUN_ID}
  FEATURE_SLUG           = kebab-case slug for TARGET from REGISTRY.md when PLAN_SCOPE=feature
  FEATURE_PATH           = {PRODUCT_ROOT}/planning-mds/features/{TARGET}-{FEATURE_SLUG} when PLAN_SCOPE=feature

SESSION_SETUP:
- Resolve {PRODUCT_ROOT} per agents/docs/AGENT-USE.md -> Session Setup
- Echo resolved absolute {PRODUCT_ROOT}
- Generate PLAN_REVIEW_RUN_ID once using YYYY-MM-DD-[a-z0-9]{8}; suffix from secrets.token_hex(4); do not use uuid4
- Create PLAN_REVIEW_RUN_FOLDER and artifacts/
- Initialize base run files per section 8: README.md, action-context.md, artifact-trace.md, gate-decisions.md, commands.log, lifecycle-gates.log

PRECONDITIONS:
- agents/actions/plan.md completed for TARGET
- Phase A and Phase B approval decisions are recorded or missing approvals are in review scope
- Tracker sync and ontology sync completed or their failures are in review scope
- TARGET resolves to concrete feature paths, feature set paths, or project planning artifacts

CONTEXT LOADING ORDER:
1. agents/ROUTER.md
2. agents/agent-map.yaml
3. agents/docs/AGENT-USE.md
4. agents/actions/plan-review.md
5. agents/actions/plan.md
6. agents/actions/feature.md
7. agents/product-manager/SKILL.md
8. agents/architect/SKILL.md
9. agents/code-reviewer/SKILL.md
10. For feature scope: FEATURE_PATH/**
11. BLUEPRINT.md, REGISTRY.md, ROADMAP.md, knowledge-graph artifacts, architecture/API/schema/security artifacts as needed

FORBIDDEN:
- Editing plan artifacts, KG artifacts, trackers, stories, contracts, schemas, architecture files, or product source files
- Writing into any feature evidence package
- Approving from prior approval tokens, summaries, or checklists without raw artifact inspection
- Treating lookup/KG mappings as authoritative over raw artifacts
- Requiring feature-assembly-plan.md as a plan deliverable
- Downgrading missing build-critical detail to low severity
- Widening review scope outside PLAN_SCOPE and TARGET except to record discovered impact

REQUIRED TOOL INVOCATIONS:
- Use lookup.py for feature routing when PLAN_SCOPE includes a feature; treat output as first-pass context only
- Append every shell command to PLAN_REVIEW_RUN_FOLDER/commands.log per section 13 JSONL schema
- Run applicable validators:
  1. python3 agents/product-manager/scripts/validate-stories.py {FEATURE_PATH}
  2. python3 agents/product-manager/scripts/validate-trackers.py
  3. python3 {PRODUCT_ROOT}/scripts/kg/validate.py
  4. python3 {PRODUCT_ROOT}/scripts/kg/validate.py --check-drift
  5. python3 agents/scripts/validate_templates.py

OWNERSHIP:
- product-manager owns: Product Readiness section findings in plan-review-report.md
- architect owns: Architecture Readiness section findings in plan-review-report.md
- code-reviewer owns: Buildability Challenge section findings in plan-review-report.md
- repair ownership remains with the original lifecycle owners through plan.md or targeted rework; reviewers do not repair during review

GATES:
- PR0 SCOPE LOCK
  - Record PLAN_SCOPE, TARGET, DIFF_RANGE, resolved paths, and boundaries in action-context.md
- PR1 PARALLEL READINESS REVIEW
  - Product Manager: requirements, stories, mutation contracts, UI/screen readiness, trackers
  - Architect: API/schema, data/workflow, authorization, ADR/NFR, KG/ontology alignment
  - Code Reviewer: vertical-slice buildability, role handoffs, testability, dependencies, risk hotspots
- PR2 VALIDATOR PASS
  - Run applicable commands listed under REQUIRED TOOL INVOCATIONS
  - Record exit code, summary, and artifact path for each command
- PR3 SELF-REVIEW GATE
  - Each reviewer verifies findings cite exact files/sections and skipped items are justified
- PR4 READINESS GATE
  - critical > 0 -> NOT READY
  - critical = 0 and high > 0 -> CONDITIONALLY READY
  - critical = 0 and high = 0 -> READY

EVIDENCE OUTPUTS:
- PLAN_REVIEW_RUN_FOLDER/README.md
- PLAN_REVIEW_RUN_FOLDER/action-context.md
- PLAN_REVIEW_RUN_FOLDER/artifact-trace.md
- PLAN_REVIEW_RUN_FOLDER/gate-decisions.md
- PLAN_REVIEW_RUN_FOLDER/commands.log
- PLAN_REVIEW_RUN_FOLDER/lifecycle-gates.log
- PLAN_REVIEW_RUN_FOLDER/plan-review-report.md
- PLAN_REVIEW_RUN_FOLDER/artifacts/* when command output is captured

PLAN-REVIEW-REPORT REQUIRED SECTIONS:
- Decision
- Findings By Severity
- Product Readiness
- Architecture Readiness
- Buildability Challenge
- Validation Evidence
- Artifact Trace

STOP CONDITIONS:
- Target scope cannot be identified
- Required raw artifacts are missing and cannot be located
- lookup.py returns only ambiguous or low-confidence matches for the declared target
- Validator failure prevents evidence-backed readiness
- Reviewers cannot cite concrete files/sections for PR4

EXIT VALIDATION:
- plan-review-report.md exists and answers "Is this plan ready to build?"
- Findings are severity-ranked and cite concrete locations
- Validator command results are recorded or justified as skipped
- README.md summarizes readiness state and open follow-ups
- gate-decisions.md records PR0 through PR4
- No product, planning, tracker, KG, source, or feature evidence artifacts were edited

CONFLICT RESOLUTION:
- Raw artifact vs KG mapping -> raw wins; record KG drift finding
- Prior approval vs current artifact gap -> current artifact gap wins
- PM and Architect disagree -> record both and escalate at PR4
- Missing build-critical owner -> NOT READY
