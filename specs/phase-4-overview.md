# Phase 4: Local Kubernetes Deployment - Detailed Specification

**Status**: Ready for Implementation
**Phase**: IV (Kubernetes & Cloud-Native)
**Hackathon Points**: 250
**Due Date**: January 4, 2026

## Overview

Transform the Phase 3 ChatKit application into a cloud-native deployment using Docker containerization and Kubernetes orchestration (Minikube) with Infrastructure-as-Code patterns via Helm charts.

## User Stories

### US-1: Deploy Frontend to Kubernetes
**As a developer**, I want to containerize the Next.js frontend application so that it can run consistently across environments.

**Acceptance Criteria:**
- [ ] Dockerfile.frontend created with multi-stage build
- [ ] Base image: `node:20-alpine`
- [ ] Development dependencies not included in production image
- [ ] Health check endpoint (`GET /`) configured
- [ ] Non-root user runs container
- [ ] Image builds without errors: `docker build -f docker/Dockerfile.frontend -t taskpilot-frontend .`
- [ ] Container starts and responds to health checks

### US-2: Deploy Backend to Kubernetes
**As a developer**, I want to containerize the FastAPI backend so that it integrates with the Kubernetes cluster.

**Acceptance Criteria:**
- [ ] Dockerfile.backend created with multi-stage build
- [ ] Base image: `python:3.13-slim`
- [ ] Requirements installed in build stage only
- [ ] Health check endpoint (`GET /health`) configured
- [ ] Non-root user runs container
- [ ] Environment variables configurable at runtime
- [ ] Image builds without errors: `docker build -f docker/Dockerfile.backend -t taskpilot-backend .`
- [ ] Container starts and connects to database

### US-3: Setup Minikube Cluster
**As a developer**, I want to initialize a local Kubernetes cluster so that I can test cloud-native deployments locally.

**Acceptance Criteria:**
- [ ] Minikube cluster starts: `minikube start --cpus 4 --memory 8192`
- [ ] kubectl configured and working
- [ ] Namespace created: `taskpilot`
- [ ] Ingress addon enabled: `minikube addons enable ingress`
- [ ] Docker images accessible to cluster
- [ ] `setup-minikube.sh` script automates initialization

### US-4: Create Helm Chart for Application
**As a developer**, I want to define infrastructure-as-code using Helm charts so that deployments are reproducible.

**Acceptance Criteria:**
- [ ] Helm chart created: `helm/taskpilot-ai/`
- [ ] Chart.yaml with proper metadata
- [ ] values.yaml with all configurable parameters
- [ ] Frontend deployment template
- [ ] Backend deployment template
- [ ] PostgreSQL StatefulSet template
- [ ] Service templates (frontend, backend, PostgreSQL)
- [ ] Ingress template for HTTP routing
- [ ] ConfigMap template for environment configuration
- [ ] Secret template for sensitive data
- [ ] `helm lint` passes without errors
- [ ] `helm install` succeeds: `helm install taskpilot-ai helm/taskpilot-ai -n taskpilot`

### US-5: Deploy Application Stack
**As a developer**, I want to deploy the entire application stack with one command so that the full environment is available for testing.

**Acceptance Criteria:**
- [ ] Frontend pod running and accessible via ingress
- [ ] Backend pod running and responding to requests
- [ ] PostgreSQL pod running with persistent storage
- [ ] All pods reach `Running` state
- [ ] Liveness probes configured
- [ ] Readiness probes configured
- [ ] Health checks passing
- [ ] Services discoverable via Kubernetes DNS
- [ ] Ingress routing requests correctly

### US-6: Configure Environment Management
**As a developer**, I want to manage configuration and secrets via ConfigMaps and Kubernetes Secrets.

**Acceptance Criteria:**
- [ ] ConfigMap created for non-sensitive configuration
- [ ] Database URL in ConfigMap
- [ ] API endpoint URL in ConfigMap
- [ ] Kubernetes Secret created for sensitive data
- [ ] OpenAI API key in Secret
- [ ] JWT secret in Secret
- [ ] Environment variables properly injected into pods
- [ ] Secrets not exposed in pod definitions
- [ ] Different values for dev/prod via Helm values overrides

### US-7: Persistent Data Storage
**As a developer**, I want the PostgreSQL database to persist data across pod restarts.

**Acceptance Criteria:**
- [ ] StatefulSet configured for PostgreSQL
- [ ] PersistentVolumeClaim created
- [ ] PersistentVolume provisioned
- [ ] Data persists after pod restart
- [ ] Volumem mount path correct: `/var/lib/postgresql/data`
- [ ] Backup strategy documented (for Phase 5)

### US-8: Horizontal Scaling
**As a developer**, I want to scale the application by increasing pod replicas.

**Acceptance Criteria:**
- [ ] Frontend replicas configurable: `frontend.replicas`
- [ ] Backend replicas configurable: `backend.replicas`
- [ ] Service load balancer distributes requests
- [ ] Helm upgrade scales pods: `helm upgrade taskpilot-ai helm/taskpilot-ai/ --set frontend.replicas=3`
- [ ] New replicas start and join service
- [ ] Health checks validate new instances
- [ ] Rolling updates don't drop connections

### US-9: Local Development Setup
**As a developer**, I want a single command to set up the entire environment locally.

**Acceptance Criteria:**
- [ ] `setup-minikube.sh` script created
- [ ] Script initializes Minikube cluster
- [ ] Script builds Docker images
- [ ] Script deploys Helm chart
- [ ] Script forwards ports for local access
- [ ] One command: `./setup.sh` sets everything up
- [ ] Application accessible at `http://localhost:3000`
- [ ] Backend API accessible at `http://localhost:8000`

### US-10: Cleanup and Reset
**As a developer**, I want to completely remove the deployment for testing fresh installations.

**Acceptance Criteria:**
- [ ] `cleanup.sh` script removes all resources
- [ ] Helm release deleted: `helm uninstall taskpilot-ai`
- [ ] Namespace deleted: `kubectl delete namespace taskpilot`
- [ ] Minikube cluster can be stopped: `minikube stop`
- [ ] Script is safe to run repeatedly (idempotent)
- [ ] No dangling resources left behind

## Functional Requirements

### Docker Containerization

#### Frontend (Next.js)
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next ./next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1
CMD ["npm", "start"]
```

**Requirements:**
- Multi-stage build (builder + production)
- Production image excludes dev dependencies
- Non-root user (nextjs:1001)
- Health check responds at `/`
- Environment variables at runtime
- Max image size: <200MB

#### Backend (FastAPI)
```dockerfile
# Stage 1: Build
FROM python:3.13-slim AS builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY backend .
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Requirements:**
- Multi-stage build
- Non-root user (appuser:1000)
- Health check at `/health` endpoint
- Environment variables configurable
- Max image size: <200MB

### Kubernetes Resources

#### Deployments
**Frontend Deployment:**
- Image: `taskpilot-frontend:latest` (local build)
- Replicas: 1-3 (configurable)
- Port: 3000
- Liveness probe: HTTP GET `/` every 30s
- Readiness probe: HTTP GET `/` immediately
- Resource requests: 100m CPU, 256Mi memory
- Resource limits: 500m CPU, 512Mi memory

**Backend Deployment:**
- Image: `taskpilot-backend:latest` (local build)
- Replicas: 1-3 (configurable)
- Port: 8000
- Liveness probe: HTTP GET `/health` every 30s
- Readiness probe: HTTP GET `/health` immediately
- Resource requests: 250m CPU, 512Mi memory
- Resource limits: 1000m CPU, 1024Mi memory
- Environment from ConfigMap and Secrets

#### StatefulSet
**PostgreSQL StatefulSet:**
- Image: `postgres:15-alpine`
- Replicas: 1 (single instance)
- Port: 5432
- PersistentVolumeClaim: 10Gi storage
- Environment: POSTGRES_PASSWORD from Secret
- Liveness probe: TCP port 5432

#### Services
**Frontend Service:**
- Type: ClusterIP
- Port: 80 → 3000
- Selector: app=taskpilot-frontend

**Backend Service:**
- Type: ClusterIP
- Port: 80 → 8000
- Selector: app=taskpilot-backend

**PostgreSQL Service:**
- Type: ClusterIP (headless for StatefulSet)
- Port: 5432 → 5432

#### Ingress
**HTTP Routing:**
- `/` routes to frontend service
- `/api/*` routes to backend service
- Host: localhost (in Minikube)
- Class: nginx

**Example:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: taskpilot-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: localhost
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80
```

### Helm Chart Structure

```
helm/taskpilot-ai/
├── Chart.yaml                          # Chart metadata
├── Chart.lock                          # Dependency lock file
├── values.yaml                         # Default values
├── values-dev.yaml                     # Dev overrides
├── values-prod.yaml                    # Prod overrides (reference)
└── templates/
    ├── _helpers.tpl                    # Template helpers
    ├── configmap.yaml                  # Configuration
    ├── secret.yaml                     # Sensitive data
    ├── frontend-deployment.yaml
    ├── backend-deployment.yaml
    ├── postgresql-statefulset.yaml
    ├── frontend-service.yaml
    ├── backend-service.yaml
    ├── postgresql-service.yaml
    ├── ingress.yaml
    ├── NOTES.txt                       # Post-install notes
    └── _post-install-jobs.yaml         # Migrations (optional)
```

### Configuration Management

**ConfigMap Values:**
```yaml
# From values.yaml
config:
  database:
    host: postgresql-service
    port: 5432
    name: taskpilot
  api:
    url: http://backend-service:8000
  frontend:
    debug: false
```

**Secret Values:**
```yaml
# From values.yaml (with placeholder)
secrets:
  openai_api_key: "{{ .Values.openaiApiKey }}"
  jwt_secret: "{{ .Values.jwtSecret }}"
  database_password: "{{ .Values.databasePassword }}"
```

### Automation Scripts

#### setup-minikube.sh
```bash
#!/bin/bash
set -e

echo "Setting up Minikube cluster..."
minikube start --cpus 4 --memory 8192 --driver docker
minikube addons enable ingress
kubectl create namespace taskpilot || true

echo "Building Docker images..."
docker build -f docker/Dockerfile.frontend -t taskpilot-frontend .
docker build -f docker/Dockerfile.backend -t taskpilot-backend .

echo "Loading images into Minikube..."
minikube image load taskpilot-frontend
minikube image load taskpilot-backend

echo "Deploying Helm chart..."
helm install taskpilot-ai helm/taskpilot-ai \
  -n taskpilot \
  --values helm/taskpilot-ai/values.yaml \
  --values helm/taskpilot-ai/values-dev.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=taskpilot-frontend -n taskpilot --timeout=300s
kubectl wait --for=condition=ready pod -l app=taskpilot-backend -n taskpilot --timeout=300s

echo "Setup complete!"
echo "Access application at: http://localhost:3000"
```

#### port-forward.sh
```bash
#!/bin/bash
echo "Forwarding ports..."
kubectl port-forward -n taskpilot svc/frontend-service 3000:80 &
kubectl port-forward -n taskpilot svc/backend-service 8000:80 &
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
wait
```

## Non-Functional Requirements

### Performance
- [ ] Frontend loads in <3 seconds
- [ ] Backend API responds in <500ms
- [ ] Horizontal scaling supports 10+ concurrent users
- [ ] Pod startup time: <30 seconds

### Reliability
- [ ] Pod restart on failure (configurable health checks)
- [ ] Graceful shutdown (30s termination grace period)
- [ ] Database data persists across restarts
- [ ] Zero data loss on pod termination

### Security
- [ ] No root user in containers
- [ ] No hardcoded secrets in images
- [ ] Secrets managed via Kubernetes Secrets
- [ ] Network policies (optional for Phase 4, implement in Phase 5)

### Maintainability
- [ ] IaC: All configuration in Git
- [ ] Reproducible: Same image SHA for all environments
- [ ] Documented: Clear setup and troubleshooting guides
- [ ] Scriptable: Automation for common tasks

## Acceptance Criteria

### Docker Requirements Met
- [ ] Frontend Dockerfile builds and runs
- [ ] Backend Dockerfile builds and runs
- [ ] Images minimal (Alpine/slim based)
- [ ] Multi-stage builds implemented
- [ ] Health checks functional
- [ ] Non-root users configured

### Kubernetes Requirements Met
- [ ] Minikube cluster running
- [ ] All pods reach Running state
- [ ] Services discoverable via DNS
- [ ] Health checks pass
- [ ] Data persists across restarts
- [ ] Horizontal scaling works

### Helm Requirements Met
- [ ] Helm chart lints successfully
- [ ] Helm install deploys correctly
- [ ] Values parameterization complete
- [ ] ConfigMaps and Secrets applied
- [ ] Post-install hooks execute (if migrations needed)

### Phase 1-3 Features Maintained
- [ ] All task CRUD operations work
- [ ] Authentication and user isolation work
- [ ] ChatKit integration works
- [ ] Real-time synchronization works

### Testing & Quality
- [ ] All Phase 1-3 tests still pass
- [ ] New K8s integration tests added
- [ ] Helm chart passes linting
- [ ] Docker images pass security scanning
- [ ] No hardcoded secrets in git

### Documentation
- [ ] Kubernetes setup guide complete
- [ ] Helm deployment guide complete
- [ ] Troubleshooting guide complete
- [ ] All scripts documented
- [ ] README updated with K8s instructions

## Implementation Steps

1. **Create Docker images** - Containerize frontend and backend
2. **Initialize Minikube** - Set up local K8s cluster
3. **Create Helm chart** - Define infrastructure-as-code
4. **Deploy application** - Use Helm to deploy stack
5. **Verify functionality** - Test all Phase 1-3 features
6. **Automate setup** - Create setup and cleanup scripts
7. **Document deployment** - Write setup and troubleshooting guides
8. **Test scaling** - Verify horizontal scaling works
9. **Security review** - Ensure no exposed secrets
10. **Final testing** - Complete integration tests

## Success Criteria

Phase 4 is complete when:
- [ ] Frontend and backend Docker images built and running
- [ ] Minikube cluster initialized and working
- [ ] Helm chart created and deployable
- [ ] Full application stack deployed in Kubernetes
- [ ] All Phase 1-3 features working in K8s
- [ ] Database persists data across restarts
- [ ] Horizontal scaling functional
- [ ] Setup and cleanup scripts working
- [ ] All quality gates passing
- [ ] Complete documentation provided
- [ ] Ready for January 4, 2026 deadline

---

**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Ready for Implementation
