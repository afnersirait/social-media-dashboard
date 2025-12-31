# Deployment Guide

## Production Deployment

### Prerequisites
- Server with Ubuntu 20.04+ or similar
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- PostgreSQL or MySQL (for production database)
- Redis server
- Nginx (for reverse proxy)

### Backend Deployment

#### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx redis-server postgresql
```

#### 2. Setup Application

```bash
# Clone repository
git clone <your-repo-url>
cd social-media-dashboard/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn
```

#### 3. Configure Environment

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/socialmedia
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=<generate-secure-random-key>
ALGORITHM=HS256
```

#### 4. Setup Database

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE socialmedia;
CREATE USER socialmedia WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE socialmedia TO socialmedia;
\q
```

#### 5. Create Systemd Service

Create `/etc/systemd/system/socialmedia-api.service`:

```ini
[Unit]
Description=Social Media Dashboard API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/social-media-dashboard/backend
Environment="PATH=/var/www/social-media-dashboard/backend/venv/bin"
ExecStart=/var/www/social-media-dashboard/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable socialmedia-api
sudo systemctl start socialmedia-api
```

### Frontend Deployment

#### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
```

#### 2. Configure Nginx

Create `/etc/nginx/sites-available/socialmedia`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/social-media-dashboard/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/socialmedia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment (Alternative)

#### 1. Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

#### 3. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./social_media.db
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  redis-data:
```

Run with:

```bash
docker-compose up -d
```

## Cloud Platform Deployment

### Heroku

#### Backend

```bash
cd backend
heroku create your-app-name-api
heroku addons:create heroku-redis:hobby-dev
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### Frontend

```bash
cd frontend
# Update VITE_API_URL in .env to your Heroku API URL
npm run build
# Deploy to Netlify, Vercel, or similar
```

### AWS

- **Backend**: Deploy to Elastic Beanstalk or ECS
- **Frontend**: Deploy to S3 + CloudFront
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache Redis

### Google Cloud Platform

- **Backend**: Cloud Run or App Engine
- **Frontend**: Cloud Storage + Cloud CDN
- **Database**: Cloud SQL
- **Cache**: Memorystore for Redis

### DigitalOcean

- **Backend**: App Platform or Droplet
- **Frontend**: App Platform (static site)
- **Database**: Managed PostgreSQL
- **Cache**: Managed Redis

## Monitoring & Maintenance

### Logging

Add logging to backend:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Checks

The API includes a health check endpoint:

```bash
curl http://your-domain.com/health
```

### Backup Strategy

#### Database Backup

```bash
# PostgreSQL
pg_dump socialmedia > backup_$(date +%Y%m%d).sql

# Automated daily backup
0 2 * * * pg_dump socialmedia > /backups/backup_$(date +\%Y\%m\%d).sql
```

#### Redis Backup

Redis automatically creates `dump.rdb` file. Copy it regularly:

```bash
cp /var/lib/redis/dump.rdb /backups/redis_$(date +%Y%m%d).rdb
```

### Performance Optimization

1. **Enable Gzip Compression** in Nginx
2. **Set up CDN** for static assets
3. **Database Indexing** on frequently queried columns
4. **Redis Cache TTL** tuning based on data freshness needs
5. **Connection Pooling** for database connections

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS everywhere
- [ ] Enable CORS only for trusted domains
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerts
- [ ] Regular backups
- [ ] Use strong database passwords

## Troubleshooting

### Backend Issues

```bash
# Check service status
sudo systemctl status socialmedia-api

# View logs
sudo journalctl -u socialmedia-api -f

# Test API directly
curl http://localhost:8000/health
```

### Frontend Issues

```bash
# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# Test Nginx configuration
sudo nginx -t
```

### Redis Issues

```bash
# Check Redis status
sudo systemctl status redis

# Test Redis connection
redis-cli ping

# View Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy, or cloud LB)
- Run multiple backend instances
- Shared Redis instance for all backends
- Centralized database

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Increase Redis memory
- Use database read replicas

### Caching Strategy

- Cache frequently accessed data
- Set appropriate TTL values
- Implement cache warming
- Use Redis clustering for large datasets
