# Kubernetes Deployment Guide

## Architecture Overview

The Social Media Dashboard is deployed as a microservices architecture on Kubernetes with the following components:

### Microservices:
1. **Frontend Service** - Vue.js SPA served by Nginx
2. **Backend Service** - FastAPI Python application
3. **Redis Service** - Caching layer

### Infrastructure Components:
- **Ingress Controller** - NGINX Ingress for routing
- **Horizontal Pod Autoscaler** - Auto-scaling based on CPU/Memory
- **Persistent Volume** - For Redis data persistence
- **Secrets Management** - Kubernetes secrets for sensitive data

## Prerequisites

### Required Tools:
- Docker
- kubectl
- Kubernetes cluster (EKS, GKE, AKS, or local with minikube/kind)
- GitHub account with packages enabled

### GitHub Secrets Required:

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```bash
KUBE_CONFIG          # Base64 encoded kubeconfig file
GITHUB_TOKEN         # Automatically provided by GitHub Actions
API_URL              # (Optional) API URL for frontend
```

### Generate KUBE_CONFIG:

```bash
# Encode your kubeconfig
cat ~/.kube/config | base64 | pbcopy  # macOS
cat ~/.kube/config | base64 -w 0      # Linux
```

## GitHub Actions Pipeline

### Pipeline Stages:

1. **Build Backend** - Builds and pushes backend Docker image
2. **Build Frontend** - Builds and pushes frontend Docker image
3. **Security Scan** - Scans images for vulnerabilities with Trivy
4. **Deploy to Kubernetes** - Deploys to staging/production based on branch

### Trigger Events:
- Push to `main` branch → Deploy to production
- Push to `develop` branch → Deploy to staging
- Pull requests → Build only (no deployment)
- Manual trigger → Via GitHub Actions UI

### Image Registry:
Images are pushed to GitHub Container Registry (ghcr.io):
- `ghcr.io/<username>/social-media-dashboard-backend:latest`
- `ghcr.io/<username>/social-media-dashboard-frontend:latest`

## Manual Deployment

### 1. Build Docker Images Locally

```bash
# Build backend
cd backend
docker build -t social-dashboard-backend:latest .

# Build frontend
cd ../frontend
docker build -t social-dashboard-frontend:latest \
  --build-arg VITE_API_URL=http://api.social-dashboard.local .
```

### 2. Push to Registry

```bash
# Tag images
docker tag social-dashboard-backend:latest ghcr.io/<username>/social-media-dashboard-backend:latest
docker tag social-dashboard-frontend:latest ghcr.io/<username>/social-media-dashboard-frontend:latest

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin

# Push images
docker push ghcr.io/<username>/social-media-dashboard-backend:latest
docker push ghcr.io/<username>/social-media-dashboard-frontend:latest
```

### 3. Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace production

# Create secrets
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=$GITHUB_TOKEN \
  --namespace=production

# Apply backend secrets
kubectl apply -f k8s/backend/secrets.yaml -n production

# Deploy Redis
kubectl apply -f k8s/redis/ -n production

# Deploy Backend
export GITHUB_REPOSITORY_OWNER=<username>
export IMAGE_TAG=latest
envsubst < k8s/backend/deployment.yaml | kubectl apply -f - -n production
kubectl apply -f k8s/backend/service.yaml -n production

# Deploy Frontend
envsubst < k8s/frontend/deployment.yaml | kubectl apply -f - -n production
kubectl apply -f k8s/frontend/service.yaml -n production

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml -n production

# Deploy HPA (optional)
kubectl apply -f k8s/hpa.yaml -n production
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n production

# Check services
kubectl get svc -n production

# Check ingress
kubectl get ingress -n production

# View logs
kubectl logs -f deployment/backend -n production
kubectl logs -f deployment/frontend -n production

# Check HPA status
kubectl get hpa -n production
```

## Configuration

### Environment Variables

#### Backend:
- `DATABASE_URL` - Database connection string
- `REDIS_HOST` - Redis hostname (default: redis)
- `REDIS_PORT` - Redis port (default: 6379)
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)

#### Frontend:
- `VITE_API_URL` - Backend API URL

### Secrets Management

For production, use one of these solutions:
- **Sealed Secrets** - Encrypt secrets in Git
- **External Secrets Operator** - Sync from external secret managers
- **HashiCorp Vault** - Centralized secrets management
- **Cloud Provider Secrets** - AWS Secrets Manager, Google Secret Manager, Azure Key Vault

Example with External Secrets Operator:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: backend-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: backend-secrets
  data:
  - secretKey: database-url
    remoteRef:
      key: social-dashboard/database-url
  - secretKey: secret-key
    remoteRef:
      key: social-dashboard/secret-key
```

## Scaling

### Horizontal Pod Autoscaler (HPA)

The HPA automatically scales pods based on CPU and memory usage:

**Backend:**
- Min replicas: 3
- Max replicas: 10
- CPU threshold: 70%
- Memory threshold: 80%

**Frontend:**
- Min replicas: 2
- Max replicas: 6
- CPU threshold: 70%
- Memory threshold: 80%

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=5 -n production

# Scale frontend
kubectl scale deployment frontend --replicas=3 -n production
```

## Monitoring

### View Metrics

```bash
# Pod metrics
kubectl top pods -n production

# Node metrics
kubectl top nodes

# HPA status
kubectl get hpa -n production --watch
```

### Recommended Monitoring Stack:
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Loki** - Log aggregation
- **Jaeger** - Distributed tracing

## Rolling Updates

### Update Backend

```bash
# Update image
kubectl set image deployment/backend \
  backend=ghcr.io/<username>/social-media-dashboard-backend:v2.0.0 \
  -n production

# Check rollout status
kubectl rollout status deployment/backend -n production

# Rollback if needed
kubectl rollout undo deployment/backend -n production
```

### Update Frontend

```bash
# Update image
kubectl set image deployment/frontend \
  frontend=ghcr.io/<username>/social-media-dashboard-frontend:v2.0.0 \
  -n production

# Check rollout status
kubectl rollout status deployment/frontend -n production
```

## Troubleshooting

### Pod Not Starting

```bash
# Describe pod
kubectl describe pod <pod-name> -n production

# View logs
kubectl logs <pod-name> -n production

# Check events
kubectl get events -n production --sort-by='.lastTimestamp'
```

### Image Pull Errors

```bash
# Verify secret
kubectl get secret ghcr-secret -n production -o yaml

# Recreate secret
kubectl delete secret ghcr-secret -n production
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=$GITHUB_TOKEN \
  --namespace=production
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n production

# Test service internally
kubectl run -it --rm debug --image=alpine --restart=Never -n production -- sh
# Inside pod:
wget -O- http://backend:8000/health
wget -O- http://frontend/health
```

### Ingress Issues

```bash
# Check ingress
kubectl describe ingress social-dashboard-ingress -n production

# View ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

## Security Best Practices

1. **Non-root containers** - All containers run as user 1000
2. **Read-only root filesystem** - Where possible
3. **Resource limits** - CPU and memory limits set
4. **Network policies** - Restrict pod-to-pod communication
5. **Pod security policies** - Enforce security standards
6. **Image scanning** - Trivy scans in CI/CD
7. **Secrets encryption** - Use external secrets management
8. **TLS/SSL** - HTTPS enforced via ingress

## Backup and Disaster Recovery

### Backup Redis Data

```bash
# Create backup
kubectl exec -it deployment/redis -n production -- redis-cli SAVE
kubectl cp production/<redis-pod>:/data/dump.rdb ./redis-backup-$(date +%Y%m%d).rdb
```

### Restore Redis Data

```bash
# Copy backup to pod
kubectl cp ./redis-backup.rdb production/<redis-pod>:/data/dump.rdb

# Restart Redis
kubectl rollout restart deployment/redis -n production
```

## Cost Optimization

1. **Right-size resources** - Adjust requests/limits based on actual usage
2. **Use HPA** - Scale down during low traffic
3. **Spot instances** - Use for non-critical workloads
4. **Resource quotas** - Prevent resource waste
5. **Image optimization** - Use multi-stage builds, alpine images

## Multi-Environment Setup

### Staging Environment

```bash
# Deploy to staging
kubectl create namespace staging
# Follow same deployment steps with staging namespace
```

### Environment-specific Configurations

Use Kustomize or Helm for environment-specific configurations:

```bash
# Kustomize example
kustomize build k8s/overlays/production | kubectl apply -f -
kustomize build k8s/overlays/staging | kubectl apply -f -
```

## Clean Up

```bash
# Delete all resources
kubectl delete namespace production

# Or delete specific resources
kubectl delete -f k8s/ -n production
```

## Support

For issues or questions:
- Check logs: `kubectl logs -f deployment/<name> -n production`
- Check events: `kubectl get events -n production`
- Review GitHub Actions logs
- Check container registry for image availability
