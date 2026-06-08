# Enterprise Architecture Decisions

Generic ADR templates and decision frameworks for enterprise service architecture. Use this reference when the Architect must justify microservices, backend stack selection, communication patterns, data stores, event sourcing, tenancy, caching, or fitness functions.

---

## 1. ADR Template with Weighted Evaluation

```markdown
# ADR-NNN: <Decision Title>

## Status
Proposed | Accepted | Superseded | Rejected

## Context
Describe the forces that require a decision. Include current constraints, affected bounded contexts, expected load, team capability, regulatory/security needs, and operational maturity.

## Decision
State the selected option in one paragraph.

## Options Considered

| Option | Summary | Pros | Cons |
|--------|---------|------|------|
| Option A |  |  |  |
| Option B |  |  |  |
| Option C |  |  |  |

## Weighted Evaluation

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Team fit | 25% |  |  |  |
| Reliability | 20% |  |  |  |
| Performance | 15% |  |  |  |
| Security | 15% |  |  |  |
| Operability | 15% |  |  |  |
| Cost | 10% |  |  |  |

Score each option from 1 to 5. Multiply by weight. Highest score wins unless a hard constraint eliminates it.

## Consequences
- Positive:
- Negative:
- Follow-up:

## Implementation Notes
- Update SOLUTION-PATTERNS.md:
- Update API/event contracts:
- Update deployment topology:
- Update test strategy:
```

---

## 2. Stack Decision ADR Example

```markdown
# ADR-003: Select Backend Stack per Service

## Status
Accepted

## Context
The product has customer, order, and product bounded contexts. The organization can operate both Python and .NET services. The architecture needs explicit stack assignment so implementation agents and CI/CD templates do not infer conflicting defaults.

## Decision
Use .NET/ASP.NET Core for customer-service and product-service because they contain type-heavy domain models and high-throughput read APIs. Use Python/FastAPI for order-service because it integrates with data-heavy workflows and async event consumers. Document the default stack and per-service overrides in SOLUTION-PATTERNS.md.

## Weighted Evaluation

| Criterion | Weight | Python/FastAPI | .NET/ASP.NET Core |
|-----------|--------|----------------|-------------------|
| Team expertise | 25% | 4 | 4 |
| Compute-bound performance | 20% | 3 | 5 |
| Data/ML ecosystem | 15% | 5 | 3 |
| I/O concurrency | 15% | 4 | 5 |
| Library availability | 10% | 4 | 4 |
| Hiring pool | 10% | 4 | 4 |
| Existing codebase momentum | 5% | 3 | 4 |

## Consequences
- Each service must have stack-specific test, packaging, and observability guidance.
- Shared contracts remain stack-neutral: OpenAPI, AsyncAPI, Avro, Protobuf, JSON Schema.
- Cross-service behavior cannot depend on language-specific object models.
```

SOLUTION-PATTERNS.md shape:

```yaml
backend_stack: polyglot
default_stack: dotnet
services:
  customer-service:
    stack: dotnet
    framework: aspnet
    database: postgresql
    justification: "ADR-003: type-heavy domain model and throughput"
  order-service:
    stack: python
    framework: fastapi
    database: postgresql
    justification: "ADR-003: data-heavy workflow and async event processing"
  product-service:
    stack: dotnet
    framework: aspnet
    database: postgresql
    justification: "ADR-003: stable catalog model and team expertise"
```

---

## 3. Microservices vs Modular Monolith ADR Example

```markdown
# ADR-001: Choose Modular Monolith or Microservices

## Status
Accepted

## Context
The system includes customer, order, and product capabilities. The decision must balance deployment independence, data ownership, team autonomy, and operational complexity.

## Options
| Option | Summary |
|--------|---------|
| Modular monolith | Single deployable, strict modules, shared database |
| Microservices | Independently deployed services, database per service |
| Hybrid | Modular monolith with one extracted service |

## Decision Criteria
| Criterion | Modular Monolith Favors | Microservices Favors |
|-----------|-------------------------|----------------------|
| Team size | One team | Multiple autonomous teams |
| Deployment | Shared cadence acceptable | Independent deploys required |
| Data | Shared relational model acceptable | Isolated stores required |
| Operations | Limited platform maturity | Mature CI/CD and observability |
| Latency | In-process calls preferred | Network boundaries acceptable |

## Decision
Start with a modular monolith unless independent deployment, independent scaling, or data sovereignty is proven for a bounded context. If microservices are selected, every service must have a context map entry, stack assignment, database ownership, contract tests, observability, and rollback path.
```

---

## 4. Event Sourcing Adoption ADR Example

```markdown
# ADR-004: Event Sourcing for Order Aggregate

## Context
The order aggregate has a complex state machine and requires a complete audit trail. Customer and product aggregates are simple CRUD models.

## Decision
Use event sourcing for order-aggregate only. Use standard relational persistence for customer-aggregate and product-aggregate.

## Decision Rule
Use event sourcing when:
- The aggregate has many meaningful transitions.
- Full state-change audit is required.
- Temporal queries are required.
- Replay has business or debugging value.

Do not use event sourcing when:
- The aggregate is simple CRUD.
- State rarely changes.
- The team cannot operate event replay and projections.
```

---

## 5. Database Selection ADR Example

```markdown
# ADR-005: Select Database per Service

## Options
| Store | Use When | Avoid When |
|-------|----------|------------|
| PostgreSQL | Relational transactions, general service database | Extreme analytical scan workloads dominate |
| Redis | Cache, ephemeral coordination, short-lived materialized state | Primary durable record is required |
| Elasticsearch | Search and text relevance | Strong consistency is required |
| ClickHouse | Analytics and high-volume columnar reads | OLTP mutations dominate |

## Decision
Default each service to PostgreSQL. Add specialized stores only when documented access patterns justify them. Specialized stores are projections or service-owned stores, not shared cross-service databases.
```

---

## 6. Communication Pattern ADR Example

```markdown
# ADR-006: Select Inter-Service Communication Patterns

## Decision Matrix
| Need | Pattern | Contract |
|------|---------|----------|
| External/public API | REST | OpenAPI |
| Internal synchronous query | gRPC | Protobuf |
| Cross-service side effect | Domain event | AsyncAPI + Avro |
| Long-running task | Command queue | AsyncAPI |
| Real-time UI | WebSocket/SignalR | Message schema |

## Decision
Use async domain events for cross-domain side effects. Use gRPC for internal synchronous queries when freshness is required in the user flow. Use REST for public APIs. Deviations require an ADR.

## Consequences
- Every event needs schema, producer, consumer, topic, versioning, and retention.
- Every synchronous dependency needs timeout, retry, circuit breaker, and fallback guidance.
- Every contract needs consumer/provider tests.
```

---

## 7. Multi-Tenancy Model ADR Example

```markdown
# ADR-007: Select Multi-Tenancy Isolation Model

## Options
| Model | Pros | Cons | Use When |
|-------|------|------|----------|
| Row-level tenant column | Low cost, simple operations | Strong policy discipline required | Most standard SaaS workloads |
| Schema per tenant | Better isolation, easier tenant export | More migration complexity | Medium isolation requirements |
| Database per tenant | Strong isolation | Higher cost and operational overhead | Enterprise isolation or compliance |
| Service per tenant | Maximum isolation | Highest cost and release complexity | Rare regulated or dedicated deployments |

## Decision
Use row-level isolation by default with mandatory tenant filters, policy tests, and audit logging. Escalate to schema or database isolation only when compliance, scale, or customer contract requires it.
```

---

## 8. Caching Strategy ADR Example

```markdown
# ADR-008: Select Caching Strategy

## Options
| Strategy | Use When | Risk |
|----------|----------|------|
| No cache | Low traffic, simple reads | Higher database load |
| In-memory cache | Single service instance or non-critical speedup | Inconsistent across replicas |
| Cache-aside Redis | Repeated reads and tolerable staleness | Invalidations must be explicit |
| Write-through cache | Cache must stay current on writes | Higher write complexity |
| Materialized projection | Cross-service read model | Event lag and projection repair |

## Decision
Default to no cache. Add cache-aside Redis only when measured latency or database saturation requires it. Specify TTL, invalidation trigger, stale-read tolerance, and metrics.
```

---

## 9. Well-Architected Review Checklist

### Reliability
- Are service dependencies identified with timeout, retry, circuit breaker, and fallback?
- Are migrations backward compatible?
- Is rollback defined for application and schema changes?
- Are SLOs and error budgets documented?

### Security
- Is authentication enforced at gateway and service?
- Are authorization checks local to the service mutation?
- Are secrets externalized and rotated?
- Is service-to-service traffic protected with mTLS when applicable?

### Performance Efficiency
- Are expected p95/p99 latency targets documented?
- Are scaling triggers and HPA metrics specified?
- Are hot paths measured before adding specialized stores?
- Are synchronous cross-service calls minimized?

### Operational Excellence
- Are traces, metrics, logs, dashboards, alerts, and runbooks defined?
- Are deployment gates automated?
- Are contract tests part of CI/CD?
- Are incident owners named by service?

### Cost Optimization
- Are replicas and resource requests justified?
- Are specialized stores justified by access pattern?
- Is canary/blue-green capacity overhead understood?
- Are non-production environments right-sized?

---

## 10. Architecture Fitness Functions

Automated or reviewable checks that keep architecture decisions enforceable:

| Fitness Function | Check |
|------------------|-------|
| Service ownership | Every service in SOLUTION-PATTERNS.md has owner, stack, database, and ADR reference |
| Contract completeness | Every REST/gRPC/event surface has OpenAPI, Protobuf, AsyncAPI, or Avro schema |
| Data sovereignty | No service reads another service database directly |
| Outbox adoption | Every published domain event is backed by transactional outbox |
| Resilience | Every synchronous service dependency has timeout and retry/circuit breaker policy |
| Observability | Every service emits traces, metrics, JSON logs, and health endpoints |
| Deployment | Every service has chart, HPA, PDB, probes, and rollback strategy |
| Security | Every mutation documents authn/authz policy and tenant isolation |

Example validation report shape:

```markdown
## Architecture Fitness Report

| Check | Status | Evidence |
|-------|--------|----------|
| Service ownership | PASS | SOLUTION-PATTERNS.md services table |
| Contract completeness | PASS | OpenAPI and AsyncAPI files |
| Data sovereignty | PASS | database-per-service section |
| Resilience | WARN | product-service fallback pending ADR |
```

---

## 11. Stack Selection Scoring Worksheet

Use this worksheet before assigning a service to Python or .NET. The Architect owns the recommendation; implementation agents consume the result.

```markdown
## Service Stack Evaluation: <service-name>

| Criterion | Weight | Evidence | Python Score | .NET Score |
|-----------|--------|----------|--------------|------------|
| Team expertise | 25% |  |  |  |
| Compute-bound performance | 20% |  |  |  |
| Data/ML ecosystem | 15% |  |  |  |
| I/O concurrency | 15% |  |  |  |
| Library availability | 10% |  |  |  |
| Hiring pool | 10% |  |  |  |
| Existing codebase momentum | 5% |  |  |  |

## Recommendation
- Selected stack:
- Framework:
- Database:
- Contract formats:
- Observability baseline:
- ADR reference:
```

Scoring guidance:
- 1: poor fit or introduces material delivery risk.
- 2: workable but needs mitigation.
- 3: neutral fit.
- 4: strong fit.
- 5: clear differentiator.

Hard eliminators:
- Team cannot operate the runtime in production.
- Required libraries are unavailable or unsupported.
- Security or compliance tooling cannot cover the stack.
- Deployment platform cannot package, scan, or observe the runtime.

---

## 12. Service Boundary Decision Worksheet

```markdown
## Boundary Evaluation: <bounded-context>

| Question | Answer | Decision Impact |
|----------|--------|-----------------|
| Can one team own this boundary end-to-end? |  |  |
| Does it need independent deployment? |  |  |
| Does it need independent scaling? |  |  |
| Does it own a distinct data lifecycle? |  |  |
| Does it require a specialized store? |  |  |
| Are its invariants local to the boundary? |  |  |
| How many synchronous dependencies would extraction create? |  |  |
| Are contract tests and tracing available? |  |  |

## Decision
Keep as module | Extract as service | Merge with adjacent boundary

## Rationale
```

Boundary warnings:
- If a workflow requires strong consistency across two proposed services, revisit the boundary.
- If most operations require synchronous calls to another service, revisit the boundary.
- If the service has no independent owner, keep it as a module.
- If two services share the same database tables, the boundary is not real.

---

## 13. Event Governance Decision Template

```markdown
# ADR-NNN: Event Governance for <topic-family>

## Context
Services publish domain events for cross-service side effects. Event contracts must evolve without breaking consumers.

## Decision
Use versioned schemas in a schema registry. Producers publish through transactional outbox. Consumers are independently deployable and tolerate unknown fields.

## Event Contract Rules
- Event names are past-tense domain facts.
- Event payloads use stable IDs, timestamps, producer service, schema version, and correlation ID.
- Producers do not publish internal entity snapshots unless the event contract explicitly requires them.
- Consumers treat events as immutable.
- Breaking changes require a new schema version and migration plan.

## Topic Shape
| Topic | Producer | Consumers | Schema | Retention | Partitions |
|-------|----------|-----------|--------|-----------|------------|
| events.orders | order-service | customer-service, product-service | Avro | 7d | 6 |

## Compatibility
Backward | Forward | Full | None
```

---

## 14. Saga Decision Template

```markdown
# ADR-NNN: Saga Strategy for <workflow>

## Context
The workflow spans multiple services and cannot use a distributed transaction.

## Decision
Use Temporal.io orchestration | Use choreography | Redesign boundary

## Workflow
| Step | Service | Action | Compensation | Timeout | Idempotency Key |
|------|---------|--------|--------------|---------|-----------------|
| 1 | order-service | Create order | Cancel order | 10s | {saga_id}:1 |
| 2 | product-service | Reserve product | Release product | 30s | {saga_id}:2 |

## Failure Handling
- Step failure:
- Timeout:
- Duplicate command:
- Partial completion:

## Test Requirements
- Unit tests for compensation decisions.
- Integration tests for timeout and duplicate messages.
- Contract tests for commands/events used by participants.
```

Prefer orchestration when:
- More than three steps exist.
- Compensation must be centrally reasoned about.
- The workflow may run for minutes, hours, or days.
- Operators need a single workflow status.

Prefer choreography when:
- The flow is two simple eventual-consistency steps.
- Failure handling is local and obvious.
- There is no central business process owner.

---

## 15. Review Questions for Architecture Approval

Ask these before Phase B approval:

- Is microservices adoption justified by ADR, or should the design stay modular monolith?
- Does every service have a bounded context, owner, stack, database, and contract surface?
- Are cross-service calls minimized and justified?
- Are all events named as domain facts and versioned through schema governance?
- Are all distributed workflows modeled as Saga, choreography, or boundary redesign?
- Are all synchronous dependencies covered by timeout, retry, circuit breaker, fallback, and metrics?
- Does every service have independent deployment and rollback guidance?
- Can QE run provider/consumer contract tests before release?
- Can DevOps deploy each service without inferring missing topology?
- Does SOLUTION-PATTERNS.md capture reusable stack and service patterns?
