# Agentignore Retrieval Policy

`.agentignore` is a product-owned retrieval guard for agent sessions. It uses
gitignore-style patterns to mark files and directories that agents must not
broad-read, broad-search, or eagerly load into context.

It is not a Git ignore file. It does not change source ownership, validation
requirements, or audit retention. It only controls agent retrieval behavior.

## Session Rule

After resolving `{PRODUCT_ROOT}`, agents must check for
`{PRODUCT_ROOT}/.agentignore` before broad product discovery. When it exists:

- Honor its patterns for broad `Read`, `Glob`, `Grep`, `rg`, and file-list
  operations.
- Prefer running product searches from `{PRODUCT_ROOT}` with
  `rg --ignore-file .agentignore ...`.
- If a tool cannot consume `.agentignore`, scope the search to known hot paths
  instead of scanning the product root.
- Do not bypass ignored paths just because a search returned no results.

## Cold Archive Rule

`{PRODUCT_ROOT}/planning-mds/operations/**` is cold archive unless the current
task explicitly needs operations evidence, run history, validation proof,
failure triage, closeout audit, or operator-requested inspection.

For evidence retrieval, start from indexes:

1. `{PRODUCT_ROOT}/planning-mds/operations/evidence/README.md`
2. `{PRODUCT_ROOT}/planning-mds/operations/evidence/features/F####-*/latest-run.json`
3. `{PRODUCT_ROOT}/planning-mds/operations/evidence/runs/{run-id}/evidence-manifest.json`

Then read only the specific evidence files named by the manifest, report, or
operator request. Do not load `{RUN_FOLDER}/**`, `artifacts/**`, legacy evidence
folders, screenshots, or logs unless the task requires that exact artifact.

## Bypass Rule

Bypass `.agentignore` only with an explicit reason:

- the user asked for an ignored path or artifact
- evidence validation or closeout audit requires it
- failure, CI, security, or quality triage needs a cited raw artifact
- a manifest or index points to an exact file needed for the current gate

When bypassing during a formal action run, record the reason and path in
`artifact-trace.md`.

## Product Context Map

Product repos may also define `{PRODUCT_ROOT}/planning-mds/context-map.yaml`.
When present, agents must treat it as the product-local prompt-loading router:

- Load only the default layers for the current action.
- Use target feature, KG lookup/hint, changed-path, manifest, exact-file, or
  explicit-user routing for on-demand layers.
- Do not load full archive, evidence, API/schema, source, test, generated,
  visual, or log surfaces unless the context map allows that route.
- Product validators may enforce this with `scripts/validate-context-map.py`.

## Product File Template

Product repos should place this file at `{PRODUCT_ROOT}/.agentignore`:

```gitignore
# Agent retrieval guard. Gitignore-style patterns for AI agents.
# This is not .gitignore; it does not change source control behavior.
#
# Broad reads/searches must honor this file. Exact-file access is still allowed
# for audits, validation, evidence review, failure triage, changed-path routing,
# KG-directed lookup, and explicit user requests.

# Dependency, generated, build, and cache outputs.
/experience/node_modules/**
/experience/dist/**
/experience/test-results/**
/experience/playwright-report/**
/experience/coverage/**
/experience/.vite/**
/engine/**/bin/**
/engine/**/obj/**
/neuron/.venv/**
/.pytest_cache/**
/.mypy_cache/**
/.ruff_cache/**
/.DS_Store

# Full runtime source trees are on-demand only. Use changed files, KG hint/lookup,
# failing test output, or exact paths instead of broad-loading whole trees.
/engine/**
/experience/src/**
/experience/tests/**
/neuron/**

# Re-allow small runtime entry points and config files for discovery.
!/engine/
!/engine/*.slnx
!/engine/**/*.csproj
!/experience/
!/experience/package.json
!/experience/vite.config.ts
!/experience/playwright.config.ts
!/experience/vitest*.config.ts
!/experience/scripts/
!/experience/scripts/**
!/neuron/
!/neuron/README.md
!/neuron/config/
!/neuron/config/*.yaml

# Treat feature archives and historical examples as cold archive by default.
/planning-mds/features/archive/**
/planning-mds/examples/**

# Re-allow feature indexes and planned feature entry points.
!/planning-mds/features/
!/planning-mds/features/REGISTRY.md
!/planning-mds/features/ROADMAP.md
!/planning-mds/features/STORY-INDEX.md
!/planning-mds/features/TRACKER-GOVERNANCE.md
!/planning-mds/features/F*/
!/planning-mds/features/F*/README.md
!/planning-mds/features/F*/feature-assembly-plan.md

# Treat operations evidence as cold archive by default.
/planning-mds/operations/**

# Re-allow only small index entry points.
!/planning-mds/operations/
!/planning-mds/operations/evidence/
!/planning-mds/operations/evidence/README.md
!/planning-mds/operations/evidence/features/
!/planning-mds/operations/evidence/features/**/
!/planning-mds/operations/evidence/features/**/latest-run.json
!/planning-mds/operations/evidence/frontend-quality/
!/planning-mds/operations/evidence/frontend-quality/README.md
!/planning-mds/operations/evidence/frontend-quality/latest-run.json
!/planning-mds/operations/evidence/frontend-ux/
!/planning-mds/operations/evidence/frontend-ux/README.md

# Large contract and architecture surfaces are on-demand exact-file context.
/planning-mds/api/**
/planning-mds/schemas/**
/planning-mds/lob-schemas/**
/planning-mds/architecture/**
/planning-mds/knowledge-graph/**

# Re-allow small routing and baseline files.
!/planning-mds/context-map.yaml
!/planning-mds/README.md
!/planning-mds/BLUEPRINT.md
!/planning-mds/api/
!/planning-mds/api/*.yaml
!/planning-mds/architecture/
!/planning-mds/architecture/SOLUTION-PATTERNS.md
!/planning-mds/architecture/api-guidelines-profile.md
!/planning-mds/architecture/api-design-guide.md
!/planning-mds/knowledge-graph/
!/planning-mds/knowledge-graph/README.md

# Visual evidence, screenshots, generated artifacts, and logs are exact-file only.
/planning-mds/screens/**
/**/*.log
/**/*.png
/**/*.jpg
/**/*.jpeg
/**/*.gif
/**/*.webp
/**/*.pdf
```
