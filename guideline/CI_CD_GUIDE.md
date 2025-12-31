# CI/CD Pipeline Guide

## Overview

This project uses GitHub Actions for continuous integration and deployment to Kubernetes. The pipeline follows microservices principles with separate build processes for frontend and backend services.

## Pipeline Architecture

```
┌─────────────────┐
│   Git Push      │
│   (main/dev)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     GitHub Actions Workflow         │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │Build Backend │  │Build Frontend│ │
│  │   Service    │  │   Service    │ │
│  └──────┬───────┘  └──────┬──────┘ │
│         │                 │        │
│         ▼                 ▼        │
│  ┌──────────────────────────────┐ │
│  │  Push to Container Registry  │ │
│  │  (GitHub Container Registry) │ │
│  └──────────────┬───────────────┘ │
│                 │                  │
│                 ▼                  │
│  ┌──────────────────────────────┐ │
│  │   Security Scan (Trivy)      │ │
│  └──────────────┬───────────────┘ │
│                 │                  │
│                 ▼                  │
│  ┌──────────────────────────────┐ │
│  │  Deploy to Kubernetes        │ │
│  │  (Staging/Production)        │ │
│  └──────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Workflow Stages

### 1. Build Backend Service

**Triggers:** Push to main/develop, Pull requests
**Duration:** ~3-5 minutes

**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Login to GitHub Container Registry
4. Extract metadata (tags, labels)
5. Build multi-platform Docker image (amd64, arm64)
6. Push to registry with appropriate tags

**Output:**
- `ghcr.io/<username>/social-media-dashboard-backend:latest`
- `ghcr.io/<username>/social-media-dashboard-backend:main-<sha>`
- `ghcr.io/<username>/social-media-dashboard-backend:<version>`

### 2. Build Frontend Service

**Triggers:** Push to main/develop, Pull requests
**Duration:** ~4-6 minutes

**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Login to GitHub Container Registry
4. Extract metadata
5. Build multi-platform Docker image with API URL
6. Push to registry

**Output:**
- `ghcr.io/<username>/social-media-dashboard-frontend:latest`
- `ghcr.io/<username>/social-media-dashboard-frontend:main-<sha>`
- `ghcr.io/<username>/social-media-dashboard-frontend:<version>`

### 3. Security Scan

**Triggers:** After successful builds
**Duration:** ~2-3 minutes

**Steps:**
1. Scan backend image with Trivy
2. Scan frontend image with Trivy
3. Upload results to GitHub Security tab
4. Fail build if critical vulnerabilities found

**Security Checks:**
- CVE vulnerabilities
- Misconfigurations
- Secrets in images
- License compliance

### 4. Deploy to Kubernetes

**Triggers:** Push to main (production) or develop (staging)
**Duration:** ~3-5 minutes

**Steps:**
1. Set up kubectl
2. Configure kubeconfig from secrets
3. Determine environment (staging/production)
4. Create namespace if not exists
5. Create Docker registry secret
6. Deploy Redis
7. Deploy Backend service
8. Deploy Frontend service
9. Deploy Ingress
10. Wait for rollout completion
11. Verify deployment

## Environment Strategy

### Staging Environment
- **Trigger:** Push to `develop` branch
- **Namespace:** `staging`
- **URL:** `https://staging.social-dashboard.example.com`
- **Replicas:** Backend: 2, Frontend: 1
- **Resources:** Lower limits for cost optimization

### Production Environment
- **Trigger:** Push to `main` branch
- **Namespace:** `production`
- **URL:** `https://social-dashboard.example.com`
- **Replicas:** Backend: 3, Frontend: 2
- **Resources:** Production-grade limits
- **Auto-scaling:** Enabled via HPA

## Required Secrets

Configure these in GitHub repository settings (Settings → Secrets and variables → Actions):

### Mandatory Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `KUBE_CONFIG` | Base64 encoded kubeconfig | `cat ~/.kube/config \| base64` |
| `GITHUB_TOKEN` | Auto-provided by GitHub | N/A |

### Optional Secrets

| Secret Name | Description | Default |
|------------|-------------|---------|
| `API_URL` | Backend API URL for frontend | `http://api.social-dashboard.local` |
| `DOCKER_USERNAME` | Docker Hub username | Uses GitHub username |
| `DOCKER_PASSWORD` | Docker Hub password | Uses GITHUB_TOKEN |

## Image Tagging Strategy

### Tag Format

```
<registry>/<owner>/<repo>-<service>:<tag>
```

### Tag Types

1. **Branch tags:** `main`, `develop`
2. **SHA tags:** `main-abc1234`, `develop-xyz5678`
3. **Semver tags:** `v1.0.0`, `v1.0`, `v1`
4. **Latest tag:** `latest` (only for main branch)
5. **PR tags:** `pr-123`

### Examples

```bash
# Production release
ghcr.io/username/social-media-dashboard-backend:latest
ghcr.io/username/social-media-dashboard-backend:v1.2.3
ghcr.io/username/social-media-dashboard-backend:main-abc1234

# Staging release
ghcr.io/username/social-media-dashboard-backend:develop
ghcr.io/username/social-media-dashboard-backend:develop-xyz5678

# Pull request
ghcr.io/username/social-media-dashboard-backend:pr-42
```

## Manual Workflow Trigger

You can manually trigger the workflow from GitHub Actions UI:

1. Go to **Actions** tab
2. Select **Build and Deploy to Kubernetes**
3. Click **Run workflow**
4. Select branch
5. Click **Run workflow** button

## Monitoring Pipeline

### View Workflow Runs

```bash
# Using GitHub CLI
gh run list
gh run view <run-id>
gh run watch <run-id>
```

### Check Build Logs

1. Go to **Actions** tab in GitHub
2. Click on workflow run
3. Click on job name
4. View step logs

### Check Deployment Status

```bash
# Check pods
kubectl get pods -n production

# Check deployment status
kubectl rollout status deployment/backend -n production
kubectl rollout status deployment/frontend -n production

# View recent events
kubectl get events -n production --sort-by='.lastTimestamp' | head -20
```

## Rollback Strategy

### Automatic Rollback

The pipeline uses rolling updates with zero downtime:
- `maxSurge: 1` - One extra pod during update
- `maxUnavailable: 0` - No pods unavailable during update

If health checks fail, Kubernetes automatically stops the rollout.

### Manual Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/backend -n production
kubectl rollout undo deployment/frontend -n production

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=2 -n production

# Check rollout history
kubectl rollout history deployment/backend -n production
```

## Performance Optimization

### Build Cache

The pipeline uses GitHub Actions cache for:
- Docker layer caching
- npm dependencies
- Python packages

### Multi-platform Builds

Images are built for both amd64 and arm64 architectures:
- Faster deployments on ARM-based nodes
- Support for Apple Silicon development
- Cost optimization with ARM instances

### Parallel Jobs

Backend and frontend builds run in parallel:
- Reduces total pipeline time
- Independent failure handling
- Efficient resource usage

## Troubleshooting

### Build Failures

**Issue:** Docker build fails

```bash
# Check build logs in GitHub Actions
# Common causes:
- Missing dependencies in requirements.txt/package.json
- Dockerfile syntax errors
- Network issues during package installation

# Solution:
- Review build logs
- Test build locally: docker build -t test .
- Check Dockerfile syntax
```

**Issue:** Image push fails

```bash
# Common causes:
- Invalid GitHub token
- Insufficient permissions
- Registry quota exceeded

# Solution:
- Verify GITHUB_TOKEN has packages:write permission
- Check registry storage quota
- Ensure repository visibility settings
```

### Deployment Failures

**Issue:** Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n production

# Common causes:
- Image pull errors
- Resource constraints
- Configuration errors

# Solution:
- Verify image exists in registry
- Check resource quotas
- Review pod logs
```

**Issue:** Health checks failing

```bash
# Check pod logs
kubectl logs <pod-name> -n production

# Common causes:
- Application not starting
- Wrong health check endpoint
- Network issues

# Solution:
- Verify application starts correctly
- Check health check configuration
- Test endpoints manually
```

## Best Practices

### 1. Version Control
- Tag releases with semantic versioning
- Use protected branches for main/develop
- Require pull request reviews

### 2. Security
- Scan images before deployment
- Use non-root containers
- Rotate secrets regularly
- Enable branch protection

### 3. Testing
- Run tests before building images
- Use staging environment for validation
- Implement smoke tests post-deployment

### 4. Monitoring
- Set up alerts for failed deployments
- Monitor resource usage
- Track deployment frequency

### 5. Documentation
- Document environment variables
- Keep deployment guide updated
- Document rollback procedures

## Advanced Configuration

### Custom Build Args

Modify `.github/workflows/build-and-deploy.yml`:

```yaml
- name: Build and push Backend image
  uses: docker/build-push-action@v5
  with:
    build-args: |
      PYTHON_VERSION=3.11
      BUILD_DATE=${{ github.event.head_commit.timestamp }}
```

### Conditional Deployments

```yaml
deploy-to-kubernetes:
  if: |
    github.ref == 'refs/heads/main' && 
    github.event_name == 'push' &&
    !contains(github.event.head_commit.message, '[skip-deploy]')
```

### Slack Notifications

Add to workflow:

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Metrics and KPIs

Track these metrics for pipeline health:

- **Build Success Rate:** Target > 95%
- **Average Build Time:** Target < 10 minutes
- **Deployment Frequency:** Track daily/weekly
- **Mean Time to Recovery:** Target < 30 minutes
- **Failed Deployment Rate:** Target < 5%

## Support

For pipeline issues:
1. Check GitHub Actions logs
2. Review this documentation
3. Check Kubernetes events
4. Contact DevOps team
5. Create GitHub issue with logs
