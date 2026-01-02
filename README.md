# Social Media Dashboard

<div align="center">

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI/CD-Automated-2088FF?logo=github-actions&logoColor=white)

**Built by [Afner Sirait](https://github.com/afnersirait)** | Full-Stack Developer

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#-quick-start)
- [Architecture](#️-architecture)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Kubernetes & CI/CD](#kubernetes--cicd)
- [Development](#development)
- [About the Developer](#about-the-developer)
- [Project Highlights](#project-highlights)

---

## 🎯 Overview

A production-ready, enterprise-grade analytics dashboard for social media management featuring real-time data visualization, intelligent post scheduling, and comprehensive engagement tracking. 

This project demonstrates modern full-stack development practices with:
- **Microservices Architecture** using Docker and Kubernetes
- **Automated CI/CD Pipeline** with GitHub Actions
- **Cloud-Native Design** with horizontal auto-scaling
- **Modern Frontend** with Vue.js 3 Composition API and dark mode
- **High-Performance Backend** with FastAPI and Redis caching

## ✨ Key Features

### Core Functionality
- 📊 **Real-time Analytics**: Interactive D3.js visualizations for engagement metrics
- 📅 **Content Scheduling**: Plan and schedule posts across multiple platforms
- 💬 **Engagement Tracking**: Monitor likes, comments, shares, and reach
- 🚀 **Performance Insights**: Track growth trends and audience demographics

### Technical Features
- ⚡ **Redis Caching**: Fast data retrieval and real-time updates
- 🎨 **Modern UI**: Responsive design with Vue.js 3 and Tailwind CSS
- 🌓 **Dark Mode**: Full dark/light theme support with persistent preferences
- ☸️ **Kubernetes Ready**: Microservices architecture with CI/CD pipeline
- 🔒 **Security**: Container scanning, non-root users, health checks
- 📈 **Auto-Scaling**: HPA-based scaling for high availability

## Tech Stack

- **Frontend**: Vue.js 3 (Composition API), Vite, Tailwind CSS, D3.js
- **Backend**: Python FastAPI, Redis, SQLite
- **Visualization**: D3.js for interactive charts
- **State Management**: Pinia
- **API**: RESTful API with WebSocket support
- **DevOps**: Docker, Kubernetes, GitHub Actions
- **Container Registry**: GitHub Container Registry (ghcr.io)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Testing)

```bash
# Clone the repository
git clone https://github.com/afnersirait/social-media-dashboard.git
cd social-media-dashboard

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Kubernetes Deployment (Production)

[![Deploy to Kubernetes](https://img.shields.io/badge/Deploy-Kubernetes-326CE5?logo=kubernetes)](guideline/QUICKSTART_K8S.md)

```bash
# Create a release to trigger deployment
gh release create v1.0.0 --title "Production Release" --notes "Initial deployment"

# Or deploy manually
kubectl apply -f k8s/ -n production
```

See [Release Deployment Guide](guideline/RELEASE_DEPLOYMENT.md) for detailed instructions.

### Option 3: Local Development

## Prerequisites

**For Local Development:**
- Node.js 18+ and npm/yarn
- Python 3.9+
- Redis server

**For Kubernetes Deployment:**
- Kubernetes cluster (EKS, GKE, AKS, or local)
- kubectl configured
- GitHub account

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/afnersirait/social-media-dashboard.git
cd social-media-dashboard
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Start Redis

```bash
# macOS (with Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Or run directly
redis-server
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ Architecture

### Microservices Design

```
┌─────────────────────────────────────────┐
│         Load Balancer / Ingress         │
│            (NGINX + TLS/SSL)            │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌──────────┐
│Frontend │      │ Backend  │
│Service  │      │ Service  │
│(Vue.js) │      │(FastAPI) │
│         │      │          │
│2-6 Pods │      │3-10 Pods │
│HPA      │      │HPA       │
└─────────┘      └────┬─────┘
                      │
                      ▼
                 ┌─────────┐
                 │  Redis  │
                 │ Service │
                 │         │
                 │ 1 Pod   │
                 │ + PVC   │
                 └─────────┘
```

### Project Structure

```
social-media-dashboard/
├── .github/
│   └── workflows/
│       └── build-and-deploy.yml    # CI/CD pipeline
├── backend/
│   ├── main.py                     # FastAPI application
│   ├── models.py                   # SQLAlchemy models
│   ├── database.py                 # Database configuration
│   ├── redis_client.py             # Redis client
│   ├── routers/                    # API endpoints
│   │   ├── analytics.py
│   │   ├── posts.py
│   │   └── accounts.py
│   ├── services/                   # Business logic
│   │   ├── analytics_service.py
│   │   └── post_service.py
│   ├── Dockerfile                  # Backend container
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── charts/
│   │   ├── views/                  # Page components
│   │   │   ├── Dashboard.vue
│   │   │   ├── Analytics.vue
│   │   │   ├── Scheduler.vue
│   │   │   ├── Posts.vue
│   │   │   └── Accounts.vue
│   │   ├── stores/                 # Pinia state management
│   │   │   ├── analytics.js
│   │   │   ├── posts.js
│   │   │   ├── accounts.js
│   │   │   └── theme.js
│   │   └── utils/                  # Helper functions
│   ├── Dockerfile                  # Frontend container
│   ├── nginx.conf                  # Nginx configuration
│   └── package.json
├── k8s/                            # Kubernetes manifests
│   ├── backend/
│   ├── frontend/
│   ├── redis/
│   ├── ingress.yaml
│   └── hpa.yaml
├── guideline/                      # Documentation
│   ├── KUBERNETES_DEPLOYMENT.md
│   ├── CI_CD_GUIDE.md
│   ├── RELEASE_DEPLOYMENT.md
│   └── DARK_MODE_COMPLETE.md
├── docker-compose.yml              # Local development
└── README.md
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=sqlite:///./social_media.db
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=your-secret-key-here
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## Features Overview

### Dashboard
- Overview of key metrics across all platforms
- Real-time engagement statistics
- Growth trends visualization

### Analytics
- Interactive charts powered by D3.js
- Platform comparison
- Audience demographics
- Peak engagement times

### Scheduler
- Calendar view for scheduled posts
- Multi-platform posting
- Draft management
- Optimal posting time suggestions

### Engagement
- Recent interactions feed
- Response management
- Sentiment analysis
- Top performing content

## Development

### Backend Development

```bash
# Run tests
pytest

# Format code
black .

# Lint
flake8
```

### Frontend Development

```bash
# Run tests
npm run test

# Lint
npm run lint

# Build for production
npm run build
```

## Kubernetes & CI/CD

### Architecture

The application follows microservices principles with three main services:
- **Frontend Service**: Vue.js SPA (Nginx)
- **Backend Service**: FastAPI Python application
- **Redis Service**: Caching layer

### CI/CD Pipeline

GitHub Actions automatically:
1. Builds Docker images for frontend and backend
2. Pushes to GitHub Container Registry
3. Scans for security vulnerabilities
4. Deploys to Kubernetes (staging/production)

### Documentation

- 📘 [Kubernetes Deployment Guide](guideline/KUBERNETES_DEPLOYMENT.md) - Complete K8s setup
- 🚀 [Quick Start Guide](guideline/QUICKSTART_K8S.md) - Deploy in 5 minutes
- 🔄 [CI/CD Guide](guideline/CI_CD_GUIDE.md) - Pipeline documentation
- � [Release Deployment](guideline/RELEASE_DEPLOYMENT.md) - Release-based deployment
- � [Docker Compose](docker-compose.yml) - Local testing
- 🌓 [Dark Mode Guide](guideline/DARK_MODE_COMPLETE.md) - Theme implementation

### Quick Commands

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/ -n production

# Scale services
kubectl scale deployment backend --replicas=5 -n production

# View logs
kubectl logs -f deployment/backend -n production

# Rollback deployment
kubectl rollout undo deployment/backend -n production
```

## About the Developer

**Afner Sirait** - Full-Stack Developer specializing in modern web applications, cloud-native architectures, and DevOps practices.

### Technical Expertise
- **Frontend**: Vue.js, React, TypeScript, Tailwind CSS
- **Backend**: Python (FastAPI, Django), Node.js
- **DevOps**: Docker, Kubernetes, CI/CD, GitHub Actions
- **Cloud**: AWS, GCP, Azure
- **Databases**: PostgreSQL, MongoDB, Redis

### Connect
- 🔗 GitHub: [@afnersirait](https://github.com/afnersirait)
- 💼 LinkedIn: [Afner Sirait](https://linkedin.com/in/afnersirait)
- 📧 Email: afner.sirait@example.com

## Project Highlights

This project demonstrates:
- ✅ **Microservices Architecture** - Scalable and maintainable design
- ✅ **Cloud-Native Development** - Kubernetes-ready with container orchestration
- ✅ **Modern Frontend** - Vue.js 3 with Composition API and dark mode
- ✅ **Robust Backend** - FastAPI with Redis caching and SQLAlchemy ORM
- ✅ **DevOps Best Practices** - Automated CI/CD, security scanning, and monitoring
- ✅ **Production-Ready** - Health checks, auto-scaling, and rollback strategies

## Contributing

While this is a personal project by Afner Sirait, suggestions and feedback are welcome! Feel free to open an issue or reach out directly.

---

**© 2025 Afner Sirait. All rights reserved.**
