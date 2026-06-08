This prompt encodes the blog action under `feature-evidence-package-standardization-plan-v2.md` (effective `2026-05-19`). Blog produces development logs, technical articles, and channel amplification content. It is OUTSIDE the feature evidence contract — it does NOT produce role reports, is NOT evidence for any completed terminal feature, and is NOT required by any validator. It still produces a base run evidence package per §8 so the blog run is auditable.

REQUIRED INPUTS (you must set):
- `POST_TYPE={devlog | technical-article | release-post | retrospective | other}`
- `TARGET_PATH={path to where the post will be written}`

OPTIONAL INPUTS (defaults apply when omitted):
- `AMPLIFICATION={none | phase-2}` — default: `none`
- `FEATURE_REF={F####}` — optional reference for read-only feature context (does NOT make this a feature-scoped run)
- `PRODUCT_ROOT=` — default: sister-repo per `agents/docs/AGENT-USE.md` → Session Setup; override only for non-standard layouts

AUTO-RESOLVED (do not set; SESSION_SETUP and the orchestrator compute these):
- `BLOG_RUN_ID` — `YYYY-MM-DD-{secrets.token_hex(4)}` generated once at session start
- `BLOG_RUN_FOLDER` — `{PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{BLOG_RUN_ID}`
- `FEATURE_REF_SLUG` — kebab-case slug for `{FEATURE_REF}` from `REGISTRY.md` (only when `FEATURE_REF` is set)
- `FEATURE_REF_PATH` — `{PRODUCT_ROOT}/planning-mds/features/{FEATURE_REF}-{FEATURE_REF_SLUG}` (only when `FEATURE_REF` is set)

Echo the resolved absolute `{PRODUCT_ROOT}` path on your first turn before any shell command.

Generate `{BLOG_RUN_ID}` once at session start using the contract format `YYYY-MM-DD-[a-z0-9]{8}` (suffix from `python3 -c "import secrets; print(secrets.token_hex(4))"`). Do not use `uuid4`.

Create `BLOG_RUN_FOLDER` at `{BLOG_RUN_FOLDER}/` and initialize the six §8 base run files from templates.

Run `agents/actions/blog.md` with `POST_TYPE`, `TARGET_PATH`, `AMPLIFICATION`, and optionally `FEATURE_REF` for context. `FEATURE_REF` does NOT make this a feature-scoped run — it is read-only context.

Load context in this order: `agents/ROUTER.md` → `agents/agent-map.yaml` → `agents/docs/AGENT-USE.md` → `agents/actions/blog.md` → `agents/blogger/SKILL.md`. For `FEATURE_REF`, also load `{FEATURE_REF_PATH}/README.md`, `{FEATURE_REF_PATH}/PRD.md`, `{FEATURE_REF_PATH}/feature-assembly-plan.md`, and (if archived) its `pm-closeout.md` — all read-only.

Don't generate `{BLOG_RUN_ID}` with `uuid4`. Don't write into any feature evidence package (`####-*/`). Don't cite a blog post as evidence for a completed terminal feature. Don't draft before the EDITORIAL BRIEF gate. Don't publish or amplify before the EDITORIAL GATE. Don't misrepresent feature status, dates, or decisions — cross-check statements against `REGISTRY.md` and `pm-closeout.md` when `FEATURE_REF` is set.

Append every shell command to `{BLOG_RUN_FOLDER}/commands.log` per the §13 JSONL schema.

Ownership: the blogger (per `agents/blogger/SKILL.md`) owns the post; the user owns approval.

Follow these gates exactly (they mirror `agents/actions/blog.md`):
- `B0 DISCOVERY` — conversational; the agent asks, recommends, and aligns with the user
- `B1 EDITORIAL BRIEF` — user approves the brief before drafting
- `B2 DRAFT` — write the primary post into `TARGET_PATH`
- `B3 SELF-REVIEW GATE` — accuracy and quality check
- `B4 EDITORIAL GATE` — user reviews and approves
- `B5 AMPLIFICATION` (optional Phase 2, only when `AMPLIFICATION=phase-2`) — produce channel derivatives

Evidence outputs land in two places. In `{BLOG_RUN_FOLDER}`: the six §8 base run files; `README.md` `Evidence Index` points to `TARGET_PATH` and any amplification artifacts; `action-context.md` records `Scope Boundaries = "Editorial content; not feature evidence"`. In `TARGET_PATH` and amplification destinations: the post and its derivatives.

Stop immediately if the user refuses the EDITORIAL BRIEF, if self-review identifies factual errors that cannot be resolved against source artifacts, or if the user refuses the EDITORIAL GATE.

Close the run by confirming `gate-decisions.md` records `B0..B5` (or `B0..B4` when `AMPLIFICATION=none`). No validators are required — blog content is not gated by feature evidence validators.

Resolve conflicts like this:
- blog statement disagrees with `REGISTRY.md`/`STATUS.md`/`pm-closeout.md` → registry/closeout wins; fix the post
- blog statement disagrees with code → code wins; do not publish content that misleads
