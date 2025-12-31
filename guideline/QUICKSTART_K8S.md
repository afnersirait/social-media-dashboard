# Kubernetes Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Prerequisites
- Kubernetes cluster running
- kubectl configured
- GitHub account

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/<your-username>/social-media-dashboard.git
cd social-media-dashboard
```

### Step 2: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add `KUBE_CONFIG`:
   ```bash
   # Generate base64 encoded kubeconfig
   cat ~/.kube/config | base64 | pbcopy  # macOS
   cat ~/.kube/config | base64 -w 0      # Linux
   ```
5. Paste the value and save

### Step 3: Push to Trigger Deployment

```bash
# Make a small change
echo "# Deployment" >> README.md

# Commit and push
git add .
git commit -m "trigger deployment"
git push origin main
```

### Step 4: Monitor Deployment

1. Go to **Actions** tab in GitHub
2. Watch the workflow run
3. Wait for all jobs to complete (~10-15 minutes)

### Step 5: Access Your Application

```bash
# Get the ingress URL
kubectl get ingress -n production

# Or use port-forward for testing
kubectl port-forward svc/frontend 8080:80 -n production
kubectl port-forward svc/backend 8000:8000 -n production

# Access at:
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

## 🧪 Test Locally with Docker Compose

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access application
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
# Redis: localhost:6379

# Seed database
curl -X POST http://localhost:8000/api/seed

# Stop services
docker-compose down
```

## 🔧 Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n production

# Expected output:
# NAME                        READY   STATUS    RESTARTS   AGE
# backend-xxx-yyy             1/1     Running   0          2m
# backend-xxx-zzz             1/1     Running   0          2m
# backend-xxx-aaa             1/1     Running   0          2m
# frontend-xxx-bbb            1/1     Running   0          2m
# frontend-xxx-ccc            1/1     Running   0          2m
# redis-xxx-ddd               1/1     Running   0          2m

# Check services
kubectl get svc -n production

# Test backend health
kubectl run -it --rm debug --image=alpine --restart=Never -n production -- sh
wget -O- http://backend:8000/health
# Should return: {"status":"healthy"}

# Test frontend
wget -O- http://frontend/health
# Should return: healthy
```

## 🎯 Seed Database

```bash
# Port forward backend
kubectl port-forward svc/backend 8000:8000 -n production

# In another terminal, seed data
curl -X POST http://localhost:8000/api/seed

# Response:
# {"message":"Database seeded successfully","accounts":4,"posts":60}
```

## 📊 View Application

```bash
# Option 1: Port Forward
kubectl port-forward svc/frontend 8080:80 -n production
# Open: http://localhost:8080

# Option 2: Configure Ingress
# Update k8s/ingress.yaml with your domain
# Then access via: https://your-domain.com
```

## 🔄 Update Application

```bash
# Make code changes
# Commit and push
git add .
git commit -m "update feature"
git push origin main

# GitHub Actions will automatically:
# 1. Build new images
# 2. Push to registry
# 3. Deploy to Kubernetes
# 4. Perform rolling update
```

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n production

# Describe problematic pod
kubectl describe pod <pod-name> -n production

# View logs
kubectl logs <pod-name> -n production
```

### Image Pull Errors

```bash
# Verify secret exists
kubectl get secret ghcr-secret -n production

# Recreate if needed
kubectl delete secret ghcr-secret -n production

# The GitHub Action will recreate it on next deployment
```

### Service Not Accessible

```bash
# Check endpoints
kubectl get endpoints -n production

# If no endpoints, check pod labels
kubectl get pods -n production --show-labels

# Verify service selector matches pod labels
kubectl get svc backend -n production -o yaml | grep selector
```

## 🧹 Clean Up

```bash
# Delete everything
kubectl delete namespace production

# Or keep namespace, delete resources
kubectl delete -f k8s/ -n production
```

## 📚 Next Steps

- [Full Kubernetes Deployment Guide](KUBERNETES_DEPLOYMENT.md)
- [CI/CD Pipeline Guide](CI_CD_GUIDE.md)
- [Main README](README.md)

## 💡 Tips

1. **Use staging first**: Test on `develop` branch before `main`
2. **Monitor resources**: Use `kubectl top pods -n production`
3. **Check HPA**: `kubectl get hpa -n production`
4. **View events**: `kubectl get events -n production --sort-by='.lastTimestamp'`
5. **Rollback if needed**: `kubectl rollout undo deployment/backend -n production`

## 🆘 Getting Help

- Check GitHub Actions logs for build issues
- Use `kubectl describe` for deployment issues
- Review pod logs with `kubectl logs`
- Check ingress controller logs for routing issues
