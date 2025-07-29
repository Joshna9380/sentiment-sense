# SentimentSense Deployment Guide

This guide provides comprehensive instructions for deploying the SentimentSense application to production.

## 🚀 Production Deployment

### Prerequisites
- Python 3.13+
- Node.js 18+
- Web server (Nginx, Apache, or cloud platform)
- Domain name (optional)

### Step 1: Backend Deployment

#### Option A: Traditional Server Deployment
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd pinnacle

# 2. Set up Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your production settings

# 4. Start production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Option B: Docker Deployment
```dockerfile
# Dockerfile for backend
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run Docker container
docker build -t sentimentsense-backend .
docker run -p 8000:8000 sentimentsense-backend
```

### Step 2: Frontend Deployment

#### Option A: Static File Hosting
```bash
# 1. Build production version
cd frontend
npm run build

# 2. Deploy build folder to web server
# Copy build/ folder to your web server's document root
```

#### Option B: Cloud Platform Deployment

**Netlify:**
```bash
# 1. Build the project
npm run build

# 2. Deploy to Netlify
netlify deploy --prod --dir=build
```

**Vercel:**
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel --prod
```

**AWS S3 + CloudFront:**
```bash
# 1. Build the project
npm run build

# 2. Upload to S3
aws s3 sync build/ s3://your-bucket-name

# 3. Configure CloudFront for CDN
```

### Step 3: Environment Configuration

#### Backend Environment Variables
```env
# Production settings
DEBUG=False
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### Frontend Environment Variables
```env
# Create .env file in frontend directory
REACT_APP_API_URL=https://your-backend-domain.com
```

### Step 4: Web Server Configuration

#### Nginx Configuration
```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/sentimentsense/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Apache Configuration
```apache
# .htaccess for frontend
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.html [QSA,L]

# Cache static assets
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 year"
</FilesMatch>
```

### Step 5: SSL/HTTPS Configuration

#### Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Step 6: Monitoring and Logging

#### Application Monitoring
```python
# Add to main.py for production logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### Health Check Endpoint
```python
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Step 7: Performance Optimization

#### Backend Optimization
```python
# Add caching headers
from fastapi.responses import JSONResponse

@app.middleware("http")
async def add_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response
```

#### Frontend Optimization
```javascript
// Add service worker for caching
// Create public/sw.js for offline functionality
```

### Step 8: Security Considerations

#### Backend Security
```python
# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_text(request: Request, text: str = Form(...)):
    # Your existing code
```

#### Frontend Security
```javascript
// Add Content Security Policy
// Add to public/index.html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

## 🔧 Troubleshooting

### Common Deployment Issues

1. **CORS Errors**: Ensure CORS_ORIGINS includes your frontend domain
2. **Static Files Not Loading**: Check web server configuration
3. **API Timeouts**: Increase timeout settings in web server
4. **Memory Issues**: Monitor server resources and optimize

### Performance Monitoring

```bash
# Monitor application performance
htop  # System resources
netstat -tulpn  # Network connections
tail -f app.log  # Application logs
```

## 📊 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend built and deployed
- [ ] SSL certificate installed
- [ ] Environment variables configured
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Security measures implemented
- [ ] Performance optimized
- [ ] Backup strategy in place
- [ ] Documentation updated

## 🎯 Deployment Platforms

### Cloud Platforms
- **Heroku**: Easy deployment with git push
- **AWS**: EC2, ECS, or Lambda
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service or Container Instances
- **DigitalOcean**: Droplets or App Platform

### Container Platforms
- **Docker**: Containerized deployment
- **Kubernetes**: Orchestrated deployment
- **Docker Compose**: Multi-service deployment

---

**Your SentimentSense application is now ready for production deployment!** 🚀 