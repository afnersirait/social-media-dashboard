# Release-Based Deployment Guide

## Overview

The CI/CD pipeline is configured to trigger **only when a new release is created** on GitHub. This ensures controlled deployments and proper version management.

## How It Works

### Trigger Events

The pipeline runs when:
- ✅ A new release is **published** on GitHub
- ✅ A new release is **created** on GitHub
- ✅ Manual trigger via GitHub Actions UI (workflow_dispatch)

The pipeline does **NOT** run on:
- ❌ Regular commits to main/develop
- ❌ Pull requests
- ❌ Branch pushes

### Environment Determination

| Release Type | Environment | Namespace | Purpose |
|--------------|-------------|-----------|---------|
| **Regular Release** | Production | `production` | Stable releases (v1.0.0, v2.1.3) |
| **Pre-release** | Staging | `staging` | Beta/RC releases (v1.0.0-beta, v2.0.0-rc1) |

## Creating a Release

### Option 1: GitHub UI (Recommended)

1. **Navigate to Releases**
   - Go to your repository on GitHub
   - Click on **"Releases"** in the right sidebar
   - Click **"Draft a new release"**

2. **Configure Release**
   - **Tag version:** Enter version (e.g., `v1.0.0`, `v1.0.1`)
   - **Target:** Select branch (usually `main`)
   - **Release title:** Enter descriptive title (e.g., "Version 1.0.0 - Initial Release")
   - **Description:** Add release notes, changelog, features
   - **Pre-release:** Check this for staging deployments (beta, RC)
   - **Set as latest release:** Check for production releases

3. **Publish Release**
   - Click **"Publish release"**
   - GitHub Actions will automatically trigger
   - Monitor deployment in the **Actions** tab

### Option 2: GitHub CLI

```bash
# Create a production release
gh release create v1.0.0 \
  --title "Version 1.0.0 - Initial Release" \
  --notes "First production release with all features" \
  --target main

# Create a pre-release (staging)
gh release create v1.1.0-beta \
  --title "Version 1.1.0 Beta" \
  --notes "Beta release for testing new features" \
  --prerelease \
  --target develop

# Create a release with auto-generated notes
gh release create v1.0.1 \
  --generate-notes \
  --target main
```

### Option 3: Git Tags + GitHub Release

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create release from tag on GitHub UI
# Or use GitHub CLI:
gh release create v1.0.0 --notes "Release notes here"
```

## Version Naming Convention

### Semantic Versioning (Recommended)

Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

**Format:** `vMAJOR.MINOR.PATCH[-PRERELEASE]`

**Examples:**
- `v1.0.0` - Major release (production)
- `v1.1.0` - Minor release with new features (production)
- `v1.1.1` - Patch release with bug fixes (production)
- `v2.0.0-beta.1` - Beta pre-release (staging)
- `v2.0.0-rc.1` - Release candidate (staging)
- `v1.2.0-alpha` - Alpha pre-release (staging)

### Version Increment Rules

| Change Type | Version Bump | Example | Environment |
|-------------|--------------|---------|-------------|
| Breaking changes | MAJOR | 1.0.0 → 2.0.0 | Production |
| New features | MINOR | 1.0.0 → 1.1.0 | Production |
| Bug fixes | PATCH | 1.0.0 → 1.0.1 | Production |
| Beta testing | PRERELEASE | 1.0.0-beta.1 | Staging |
| Release candidate | PRERELEASE | 1.0.0-rc.1 | Staging |

## Deployment Workflow

### Complete Release Process

```
1. Development
   ↓
2. Code Review & Testing
   ↓
3. Create Pre-release (v1.0.0-beta)
   ↓
4. GitHub Actions Triggers
   ↓
5. Deploy to Staging
   ↓
6. QA Testing in Staging
   ↓
7. Create Production Release (v1.0.0)
   ↓
8. GitHub Actions Triggers
   ↓
9. Deploy to Production
   ↓
10. Monitor & Verify
```

### Pipeline Stages

When a release is created, the pipeline:

1. **Build Backend**
   - Builds Docker image
   - Tags with release version
   - Pushes to ghcr.io

2. **Build Frontend**
   - Builds Docker image
   - Tags with release version
   - Pushes to ghcr.io

3. **Security Scan**
   - Scans images for vulnerabilities
   - Reports to GitHub Security

4. **Deploy to Kubernetes**
   - Determines environment (staging/production)
   - Deploys to appropriate namespace
   - Uses release tag for images
   - Performs rolling update
   - Verifies deployment

## Monitoring Deployment

### View Pipeline Progress

```bash
# Using GitHub CLI
gh run list
gh run watch

# Or visit GitHub Actions tab in browser
```

### Check Deployment Status

```bash
# Check pods
kubectl get pods -n production
kubectl get pods -n staging

# Check deployment
kubectl rollout status deployment/backend -n production
kubectl rollout status deployment/frontend -n production

# View logs
kubectl logs -f deployment/backend -n production
```

## Rollback Strategy

### Rollback to Previous Release

If a deployment fails or has issues:

**Option 1: Kubernetes Rollback**
```bash
# Rollback to previous version
kubectl rollout undo deployment/backend -n production
kubectl rollout undo deployment/frontend -n production

# Rollback to specific revision
kubectl rollout history deployment/backend -n production
kubectl rollout undo deployment/backend --to-revision=2 -n production
```

**Option 2: Create Rollback Release**
```bash
# Create a new release with previous version
gh release create v1.0.2 \
  --title "Rollback to v1.0.1" \
  --notes "Rolling back due to issues in v1.0.2" \
  --target main
```

## Best Practices

### 1. Pre-release Testing

Always test in staging before production:

```bash
# Create pre-release
gh release create v1.1.0-beta \
  --prerelease \
  --notes "Testing new features"

# After testing, create production release
gh release create v1.1.0 \
  --notes "Stable release with new features"
```

### 2. Release Notes

Include comprehensive release notes:

```markdown
## What's New
- Feature: Dark mode support
- Feature: Kubernetes deployment
- Enhancement: Improved performance

## Bug Fixes
- Fixed: Text readability in dark mode
- Fixed: Chart loading issues

## Breaking Changes
- API endpoint /old-endpoint removed

## Upgrade Notes
- Run database migrations before deploying
```

### 3. Changelog Maintenance

Keep a CHANGELOG.md file:

```markdown
# Changelog

## [1.1.0] - 2025-01-15
### Added
- Dark mode toggle
- Kubernetes deployment support

### Fixed
- Text contrast in dark mode
```

### 4. Version Tagging

```bash
# Always use annotated tags
git tag -a v1.0.0 -m "Release version 1.0.0"

# Include release notes in tag
git tag -a v1.0.0 -m "$(cat RELEASE_NOTES.md)"

# Push tags
git push origin v1.0.0
```

## Manual Deployment Trigger

If you need to deploy without creating a release:

1. Go to **Actions** tab
2. Select **"Build and Deploy to Kubernetes"**
3. Click **"Run workflow"**
4. Select branch
5. Click **"Run workflow"** button

**Note:** Manual triggers will use the latest code from the selected branch.

## Image Tags

The pipeline creates multiple image tags:

| Tag Type | Example | Purpose |
|----------|---------|---------|
| Release version | `v1.0.0` | Specific release |
| Major.Minor | `v1.0` | Latest patch in minor version |
| Major | `v1` | Latest minor in major version |
| Latest | `latest` | Latest production release |

**Example for release v1.2.3:**
```
ghcr.io/username/social-media-dashboard-backend:v1.2.3
ghcr.io/username/social-media-dashboard-backend:v1.2
ghcr.io/username/social-media-dashboard-backend:v1
ghcr.io/username/social-media-dashboard-backend:latest
```

## Troubleshooting

### Release Not Triggering Pipeline

**Check:**
- Release is published (not draft)
- GitHub Actions is enabled
- Workflow file is in `.github/workflows/`
- No syntax errors in workflow YAML

**Solution:**
```bash
# Verify workflow file
cat .github/workflows/build-and-deploy.yml

# Check GitHub Actions status
gh workflow list
gh workflow view "Build and Deploy to Kubernetes"
```

### Deployment Fails

**Check:**
- KUBE_CONFIG secret is set correctly
- Kubernetes cluster is accessible
- Images were built successfully
- Resource quotas not exceeded

**Solution:**
```bash
# Check GitHub Actions logs
gh run view --log

# Check Kubernetes events
kubectl get events -n production --sort-by='.lastTimestamp'

# Check pod status
kubectl describe pod <pod-name> -n production
```

### Wrong Environment Deployed

**Issue:** Pre-release deployed to production

**Cause:** Pre-release checkbox not selected

**Solution:**
- Delete the release
- Recreate with pre-release checkbox enabled
- Or manually move pods:
  ```bash
  kubectl get deployment backend -n production -o yaml > backend.yaml
  # Edit namespace to staging
  kubectl apply -f backend.yaml
  ```

## Examples

### Example 1: First Production Release

```bash
# 1. Ensure code is tested
git checkout main
git pull origin main

# 2. Create release
gh release create v1.0.0 \
  --title "Version 1.0.0 - Initial Production Release" \
  --notes "First stable release with all core features" \
  --target main

# 3. Monitor deployment
gh run watch

# 4. Verify
kubectl get pods -n production
```

### Example 2: Beta Release for Testing

```bash
# 1. Create pre-release
gh release create v1.1.0-beta \
  --title "Version 1.1.0 Beta - New Features" \
  --notes "Testing new analytics features" \
  --prerelease \
  --target develop

# 2. Test in staging
kubectl port-forward svc/frontend 8080:80 -n staging

# 3. If successful, create production release
gh release create v1.1.0 \
  --title "Version 1.1.0 - New Analytics Features" \
  --notes "Stable release with new analytics" \
  --target main
```

### Example 3: Hotfix Release

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug main

# 2. Fix bug and commit
git commit -am "Fix critical security issue"

# 3. Merge to main
git checkout main
git merge hotfix/critical-bug
git push origin main

# 4. Create patch release
gh release create v1.0.1 \
  --title "Version 1.0.1 - Security Hotfix" \
  --notes "Critical security patch" \
  --target main
```

## Summary

✅ **Controlled Deployments** - Only via releases
✅ **Version Management** - Semantic versioning
✅ **Environment Separation** - Staging vs Production
✅ **Automated Pipeline** - Build, scan, deploy
✅ **Rollback Support** - Easy version rollback
✅ **Audit Trail** - All deployments tracked

For more information, see:
- [CI/CD Guide](CI_CD_GUIDE.md)
- [Kubernetes Deployment](KUBERNETES_DEPLOYMENT.md)
- [Quick Start](QUICKSTART_K8S.md)
