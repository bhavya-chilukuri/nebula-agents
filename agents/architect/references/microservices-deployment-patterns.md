# Microservices Deployment Patterns

Generic deployment and operations patterns for enterprise microservices. Use this reference when the Architect must specify Kubernetes topology, Helm packaging, service mesh behavior, CI/CD gates, release strategies, secrets, observability, and operational runbooks.

---

## 1. Deployment Principles

- Every service is independently buildable, testable, deployable, observable, and rollbackable.
- Runtime configuration comes from environment variables, ConfigMaps, Secrets, or external secret stores.
- Each service owns its database migrations and runs them through a controlled deployment step.
- Contract tests must pass before a provider deploys a breaking API or event change.
- Production deployment requires SLO dashboards, alerts, runbooks, and rollback instructions.
- Services should fail fast on missing required configuration and expose health, readiness, and metrics endpoints.

---

## 2. Multi-Stage Dockerfiles

### 2.1 Python/FastAPI

```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

FROM base AS build
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM base AS runtime
COPY --from=build /app/.venv /app/.venv
COPY app ./app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 .NET/ASP.NET Core

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY CustomerService.csproj ./
RUN dotnet restore CustomerService.csproj
COPY . ./
RUN dotnet publish CustomerService.csproj -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /out ./
EXPOSE 8080
ENTRYPOINT ["dotnet", "CustomerService.dll"]
```

---

## 3. Kubernetes Resource Pattern

Each service gets a Deployment, Service, HPA, PDB, ConfigMap, Secret reference, NetworkPolicy, and optional Ingress route.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  labels:
    app: order-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: registry.example.com/order-service:1.0.0
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: order-service-config
            - secretRef:
                name: order-service-secret
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 20
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - name: http
      port: 80
      targetPort: 8000
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-service
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: order-service
```

---

## 4. Configuration and Secrets

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
data:
  ENVIRONMENT: production
  OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector:4317
  KAFKA_BOOTSTRAP_SERVERS: kafka:9092
```

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: order-service-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: platform-secret-store
    kind: ClusterSecretStore
  target:
    name: order-service-secret
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: services/order-service/database-url
```

Rules:
- Never store raw secret values in Git.
- Prefer External Secrets Operator or Vault Agent sidecars for production.
- Rotate credentials independently per service.
- Keep database credentials service-specific.

---

## 5. Helm Chart Structure

Use one chart per service when services deploy independently. Use umbrella charts only for local development or tightly coupled preview environments.

```text
deploy/
  helm/
    order-service/
      Chart.yaml
      values.yaml
      values-dev.yaml
      values-staging.yaml
      values-prod.yaml
      templates/
        deployment.yaml
        service.yaml
        hpa.yaml
        pdb.yaml
        configmap.yaml
        externalsecret.yaml
        ingress.yaml
        networkpolicy.yaml
```

```yaml
# values.yaml
image:
  repository: registry.example.com/order-service
  tag: "1.0.0"

replicaCount: 2

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

---

## 6. Service Mesh

Use a service mesh when the platform needs mTLS, traffic policies, retries, circuit breaking, canary traffic shifting, or detailed service-to-service telemetry.

### 6.1 Istio mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default-strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### 6.2 Traffic Policy

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: order-service
spec:
  host: order-service
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 100
        maxRequestsPerConnection: 50
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
```

### 6.3 Canary Routing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
    - order-service
  http:
    - route:
        - destination:
            host: order-service
            subset: stable
          weight: 90
        - destination:
            host: order-service
            subset: canary
          weight: 10
```

---

## 7. CI/CD Pipeline

Each service pipeline should run:

1. Static checks and dependency audit
2. Unit tests
3. Integration tests with Testcontainers
4. Contract tests for consumed and provided APIs/events
5. Container build and image scan
6. Helm template validation
7. Deploy to dev
8. Smoke tests
9. Promote to staging
10. Canary or blue/green production release with metric gate

```yaml
pipeline:
  service: order-service
  gates:
    - lint
    - unit_tests
    - integration_tests
    - contract_tests
    - image_scan
    - helm_template
    - dev_smoke
    - staging_smoke
    - production_metric_gate
```

Contract gate rule:
- Provider changes must verify every active consumer contract.
- Consumer changes must publish updated expectations before provider rollout.
- Breaking event schema changes require versioned topics or versioned schema subjects.

---

## 8. Blue/Green Deployment

Blue/green is useful when rollback must be instant and capacity can temporarily double.

```yaml
blue_green:
  active: blue
  candidate: green
  validation:
    - health_checks
    - smoke_tests
    - synthetic_transactions
    - dashboard_slo_check
  switch:
    method: gateway_route_flip
  rollback:
    method: route_flip_to_previous
    max_time: 5m
```

Architecture requirements:
- Database migrations must be backward compatible.
- Events must be backward compatible during the cutover window.
- Both versions must accept the same authentication and routing headers.

---

## 9. Canary Deployment

Canary is useful when gradual exposure and metric-based promotion reduce release risk.

```yaml
canary:
  stages:
    - weight: 5
      duration: 10m
    - weight: 25
      duration: 20m
    - weight: 50
      duration: 30m
    - weight: 100
      duration: complete
  abort_if:
    error_rate: "> 1%"
    p99_latency: "> 1000ms"
    availability: "< 99.9%"
```

Metric gate inputs:
- Request success rate
- p95/p99 latency
- Error budget burn rate
- Kafka consumer lag
- Saturation metrics (CPU, memory, thread pool, connection pool)

---

## 10. GitOps

Use ArgoCD or Flux when deployment state should be declarative and auditable.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: order-service
spec:
  project: services
  source:
    repoURL: https://example.com/platform-deployments.git
    targetRevision: main
    path: deploy/helm/order-service
    helm:
      valueFiles:
        - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 11. Database Migrations in Kubernetes

Migration strategy:
- Run migrations as a pre-deploy job, not in every application pod.
- Use advisory locks or migration tooling locks.
- Prefer backward-compatible expand/contract migrations.
- Separate schema expansion, code rollout, and schema contraction.

Python:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: order-service-migrate
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.example.com/order-service:1.0.0
          command: ["alembic", "upgrade", "head"]
          envFrom:
            - secretRef:
                name: order-service-secret
```

.NET:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: customer-service-migrate
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.example.com/customer-service:1.0.0
          command: ["dotnet", "CustomerService.Migrations.dll"]
          envFrom:
            - secretRef:
                name: customer-service-secret
```

---

## 12. Observability and Incident Response

Minimum production requirements:
- Prometheus metrics scraped every 15 seconds.
- OpenTelemetry traces exported through an OTLP collector.
- JSON logs aggregated in Loki or Elasticsearch.
- Every request has `trace_id`, `span_id`, and `request_id`.
- Alert rules map to runbooks.
- On-call escalation matrix exists for every service.

```yaml
runbook:
  service: order-service
  alerts:
    high_error_rate:
      impact: users may be unable to create orders
      first_checks:
        - inspect recent deployment
        - check database connectivity
        - check kafka producer errors
      rollback:
        - revert canary to stable
        - redeploy previous image if route flip fails
```

---

## 13. Architect Output Checklist

- Kubernetes namespace strategy is specified.
- Every service has Deployment, Service, HPA, PDB, ConfigMap, Secret source, and NetworkPolicy guidance.
- Every service has independent image, chart, and deployment version.
- Migration strategy is documented per service.
- Release strategy is blue/green, canary, or rolling with explicit rollback path.
- Service mesh mTLS and traffic policy requirements are documented when needed.
- CI/CD gates include contract tests and image scanning.
- Observability includes traces, metrics, logs, dashboards, alerts, and runbooks.

---

## 14. Environment Promotion Model

Use the same artifact through every environment. Promotion changes configuration and deployment intent, not the container image.

```yaml
promotion:
  image_immutability: true
  environments:
    dev:
      approval: automated
      required_gates: [unit_tests, integration_tests, contract_tests]
    staging:
      approval: team_lead
      required_gates: [smoke_tests, migration_dry_run, synthetic_checks]
    prod:
      approval: release_owner
      required_gates: [canary_metrics, rollback_plan, runbook_ready]
```

Rules:
- Dev may deploy on every accepted change.
- Staging should mirror production topology at smaller scale.
- Production requires explicit rollback and metric gates.
- Manual gates should record who approved, when, and which artifact was promoted.

---

## 15. Network Policy Pattern

Default deny ingress and egress, then allow only documented service relationships.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-policy
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: kafka
      ports:
        - protocol: TCP
          port: 9092
```

Architect decision output should map each allowed network path to a communication topology entry.

---

## 16. Readiness Review

Before approving production deployment, verify:

- All services expose `/health/live`, `/health/ready`, and `/metrics` or equivalent endpoints.
- Dashboards cover request rate, error rate, duration, saturation, dependency latency, and queue lag.
- Alerts have runbooks and owners.
- Migrations are backward compatible or have an approved maintenance plan.
- Rollback has been tested in staging.
- Canary or blue/green metrics are defined before rollout.
- Contract tests pass for every provider and consumer pair.
- Secrets are sourced from external secret management.
- Network policies and service mesh policies match the architecture topology.
- Incident response includes escalation, customer-impact assessment, and communication owner.
