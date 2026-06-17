This prompt encodes the document action under the Feature Evidence Contract in `CONSUMER-CONTRACT.md` (effective `2026-05-19`). Document produces technical documentation (API docs, READMEs, runbooks, developer guides). It is OUTSIDE the feature evidence contract — it does NOT produce role reports for any feature evidence package and does NOT substitute for evidence on a completed terminal feature. It still produces a base run evidence package per §8 so the documentation run itself is auditable.

REQUIRED INPUTS (you must set):
- `DOC_SCOPE={api | readme | runbook | developer-guide | release-notes | mixed}`
- `TARGETS=[{path}, ...]` — destination doc files

OPTIONAL INPUTS (defaults apply when omitted):
- `SOURCE_CODE=[{path}, ...]` — source code basis for the docs (default: derived from `TARGETS`)
- `FEATURE_REF={F####}` — optional reference for read-only feature context (does NOT make this a feature-scoped run)
- `PRODUCT_ROOT=` — default: sister-repo per `agents/docs/AGENT-USE.md` → Session Setup; override only for non-standard layouts

AUTO-RESOLVED (do not set; SESSION_SETUP and the orchestrator compute these):
- `DOC_RUN_ID` — `YYYY-MM-DD-{secrets.token_hex(4)}` generated once at session start
- `DOC_RUN_FOLDER` — `{PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{DOC_RUN_ID}`
- `FEATURE_REF_SLUG` — kebab-case slug for `{FEATURE_REF}` from `REGISTRY.md` (only when `FEATURE_REF` is set)
- `FEATURE_REF_PATH` — `{PRODUCT_ROOT}/planning-mds/features/{FEATURE_REF}-{FEATURE_REF_SLUG}` (only when `FEATURE_REF` is set)

Echo the resolved absolute `{PRODUCT_ROOT}` path on your first turn before any shell command.

Generate `{DOC_RUN_ID}` once at session start using the contract format `YYYY-MM-DD-[a-z0-9]{8}` (suffix from `python3 -c "import secrets; print(secrets.token_hex(4))"`). Do not use `uuid4`.

Create `DOC_RUN_FOLDER` at `{DOC_RUN_FOLDER}/` and initialize the six §8 base run files from templates.

Run `agents/actions/document.md` with `DOC_SCOPE`, `TARGETS`, optionally `SOURCE_CODE`, and optionally `FEATURE_REF` for context only — `FEATURE_REF` does NOT make this a feature-scoped run.

Load context in this order: `agents/ROUTER.md` → `agents/agent-map.yaml` → `agents/docs/AGENT-USE.md` → `agents/actions/document.md` → `agents/technical-writer/SKILL.md` → `SOURCE_CODE` paths read-only → for `FEATURE_REF`, `{FEATURE_REF_PATH}/README.md`, `{FEATURE_REF_PATH}/PRD.md`, and `{FEATURE_REF_PATH}/feature-assembly-plan.md` read-only.

Don't generate `{DOC_RUN_ID}` with `uuid4`. Don't write into any feature evidence package (`####-*/`). Don't cite documentation as a substitute for required feature evidence reports such as `test-execution-report.md` or `code-review-report.md`. Don't execute compile/lint/runtime commands outside runtime containers. Don't skip the SELF-REVIEW or APPROVAL gates from `agents/actions/document.md`.

Append every shell command to `{DOC_RUN_FOLDER}/commands.log` per the §13 JSONL schema. Runtime verifications (API examples, CLI commands, health checks) run in runtime containers when feasible and their artifact paths are recorded.

Ownership is simple: the technical writer (per `agents/technical-writer/SKILL.md`) owns every produced doc file.

Follow these gates exactly:
- `D0 SCOPE LOCK` — confirm `DOC_SCOPE`, `TARGETS`, `SOURCE_CODE`; record in `gate-decisions.md`
- `D1 DRAFT` — produce or update the `TARGETS`
- `D2 SELF-REVIEW GATE` — author validates documentation quality and accuracy
- `D3 APPROVAL GATE` — user reviews documentation

Evidence outputs land in two places. In `{DOC_RUN_FOLDER}`: the six §8 base run files; the `README.md` `Evidence Index` should point to `TARGETS`; `action-context.md` records `Scope Boundaries = "Documentation only; not feature evidence"`. In `TARGETS`: the documentation files themselves, with format and headings appropriate to the doc type.

Stop immediately if self-review identifies factual errors that cannot be resolved against the source code, if a runtime verification fails and the doc would mislead users, or if approval is refused by the user.

Close the run by executing these in order, each exit 0:
- `python3 agents/scripts/validate_templates.py`
- `python3 {PRODUCT_ROOT}/scripts/kg/validate.py --check-drift` (only required when KG references changed)

Do NOT call `validate-feature-evidence.py` — there is no feature evidence package for this run.

Resolve conflicts like this:
- doc disagrees with code → code wins; update the doc, not the code
- doc disagrees with API contract → contract wins; route to plan or architect if the contract itself is wrong
- doc cites a runtime example that does not work → fix or remove the example; do not ship docs that mislead
