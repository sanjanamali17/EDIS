# 🚀 EDIS Deployment Guide - Real-Time Production Setup

## 📋 Deployment Overview

**Deploying EDIS for real-time use requires setting up production servers, databases, and monitoring systems.** This guide covers multiple deployment options from simple to enterprise-level.

---

## 🎯 Deployment Options

### **1. 🏠 Simple Local Deployment**
- **Best for**: Development, testing, small teams
- **Cost**: Free (using your own machine)
- **Setup time**: 30 minutes
- **Scalability**: Limited to your machine resources

### **2. ☁️ Cloud Platform Deployment**
- **Best for**: Production, multiple users, global access
- **Cost**: $20-200/month depending on usage
- **Setup time**: 2-4 hours
- **Scalability**: Automatic scaling

### **3. 🏢 Enterprise Deployment**
- **Best for**: Organizations, government agencies, large teams
- **Cost**: $500-5000/month
- **Setup time**: 1-2 weeks
- **Scalability**: High availability, load balancing

---

## 🏠 Option 1: Simple Local Deployment

### **📋 Prerequisites**
- **Windows/Linux/macOS** machine with internet
- **Python 3.8+** and **Node.js 16+** installed
- **4GB+ RAM** and **20GB+ storage**
- **Stable internet connection**

### **🔧 Setup Steps**

#### **Step 1: Backend Setup**
```bash
# Navigate to backend directory
cd EDIS1/backend

# Install production dependencies
pip install fastapi uvicorn gunicorn requests pandas numpy scikit-learn joblib groq python-dotenv reportlab

# Create production environment file
cp .env .env.production

# Start production server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

#### **Step 2: Frontend Setup**
```bash
# Navigate to frontend directory
cd EDIS_/edis-dashboard

# Install dependencies
npm install

# Build for production
npm run build

# Serve built files
npx serve dist -l 3000
```

#### **Step 3: Network Configuration**
```bash
# Find your local IP
ipconfig (Windows) or ifconfig (Linux/macOS)

# Allow firewall access
# Windows: Allow ports 8000 and 3000 in Windows Firewall
# Linux: sudo ufw allow 8000 && sudo ufw allow 3000
```

#### **Step 4: Access Your EDIS**
- **Frontend**: `http://YOUR_LOCAL_IP:3000`
- **Backend**: `http://YOUR_LOCAL_IP:8000`
- **API Docs**: `http://YOUR_LOCAL_IP:8000/docs`

### **🔒 Security Setup**
```bash
# Create .env.production with secure settings
GROQ_API_KEY=your_actual_groq_key
DEBUG=false
ALLOWED_HOSTS=your_local_ip,localhost
```

---

## ☁️ Option 2: Cloud Platform Deployment

### **🌐 Recommended Platforms**

#### **A. 🐳 Docker + Cloud Server (Recommended)**
- **Providers**: DigitalOcean, AWS, Google Cloud
- **Cost**: $20-50/month
- **Performance**: Excellent
- **Control**: Full control

#### **B. 🚀 Vercel + Railway (Easiest)**
- **Frontend**: Vercel (free tier available)
- **Backend**: Railway (free tier available)
- **Cost**: $0-30/month
- **Setup**: 30 minutes

#### **C. ⚡ Heroku (Quick Start)**
- **All-in-one**: Frontend + backend
- **Cost**: $25-100/month
- **Setup**: 15 minutes
- **Limitations**: Less control

---

## 🐳 Docker Deployment (Recommended)

### **📦 Create Dockerfiles**

#### **Backend Dockerfile**
```dockerfile
# EDIS1/backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
```

#### **Frontend Dockerfile**
```dockerfile
# EDIS_/edis-dashboard/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### **docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./EDIS1/backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DEBUG=false
    volumes:
      - ./EDIS1/data:/app/data

  frontend:
    build: ./EDIS_/edis-dashboard
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
```

### **🚀 Deployment Commands**
```bash
# Build and start containers
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## 🚀 Vercel + Railway Deployment

### **📱 Frontend Deployment (Vercel)**

#### **Step 1: Prepare Frontend**
```bash
# Update API URL in frontend
cd EDIS_/edis-dashboard

# Create .env.production
REACT_APP_API_URL=https://your-railway-app.railway.app

# Build for production
npm run build
```

#### **Step 2: Deploy to Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Follow prompts to connect your GitHub account
```

### **🔧 Backend Deployment (Railway)**

#### **Step 1: Prepare Backend**
```bash
# Navigate to backend
cd EDIS1/backend

# Create railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[env]
GROQ_API_KEY = "${GROQ_API_KEY}"
DEBUG = "false"
```

#### **Step 2: Deploy to Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables
railway variables set GROQ_API_KEY=your_groq_key
```

---

## 🏢 Enterprise Deployment

### **🏗️ Infrastructure Setup**

#### **🔧 Load Balancer (Nginx)**
```nginx
# /etc/nginx/sites-available/edis
upstream edis_backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    server_name edis.yourcompany.com;

    location /api/ {
        proxy_pass http://edis_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/edis;
        try_files $uri $uri/ /index.html;
    }
}
```

#### **🗄️ Database Setup (PostgreSQL)**
```sql
-- Create database for production
CREATE DATABASE edis_production;

-- Create user
CREATE USER edis_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE edis_production TO edis_user;

-- Connect and create tables
\c edis_production
```

#### **🔒 SSL Certificate (Let's Encrypt)**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d edis.yourcompany.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Real-Time Data Integration

### **🛰️ API Integration for Live Data**

#### **Weather API Integration**
```python
# backend/services/weather_service.py
import requests

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5'

    def get_current_weather(self, lat, lon):
        url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        return response.json()

    def get_forecast(self, lat, lon, days=7):
        url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        return response.json()
```

#### **Satellite Data Integration**
```python
# backend/services/satellite_service.py
import ee

class SatelliteService:
    def __init__(self):
        ee.Initialize()
        self.collection = 'LANDSAT/LC08/C01/T1_SR'

    def get_ndvi(self, lat, lon, start_date, end_date):
        point = ee.Geometry.Point([lon, lat])
        collection = ee.ImageCollection(self.collection) \
            .filterBounds(point) \
            .filterDate(start_date, end_date) \
            .select(['NDVI'])
        
        return collection.getRegion(point, 30).getInfo()
```

### **⚡ Real-Time Updates**

#### **WebSocket Implementation**
```python
# backend/websocket_manager.py
from fastapi import WebSocket
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_update(self, data: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(data))

manager = WebSocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process real-time updates
    except:
        manager.disconnect(websocket)
```

---

## 🔍 Monitoring & Logging

### **📈 Application Monitoring**

#### **Prometheus + Grafana Setup**
```yaml
# monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
```

#### **Health Check Endpoints**
```python
# backend/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "ml_models": "loaded",
            "ai_assistant": "active"
        }
    }

@router.get("/metrics")
async def metrics():
    return {
        "active_users": get_active_users(),
        "api_calls_today": get_api_calls(),
        "prediction_accuracy": get_model_accuracy(),
        "response_time": get_avg_response_time()
    }
```

---

## 🔒 Security Hardening

### **🛡️ Production Security**

#### **Environment Variables**
```bash
# .env.production
GROQ_API_KEY=your_secure_groq_key
DATABASE_URL=postgresql://edis_user:secure_password@localhost:5432/edis_production
JWT_SECRET=your_jwt_secret_key
DEBUG=false
ALLOWED_HOSTS=edis.yourdomain.com,www.edis.yourdomain.com
CORS_ORIGINS=https://edis.yourdomain.com,https://www.edis.yourdomain.com
```

#### **Rate Limiting**
```python
# backend/middleware/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/analyze")
@limiter.limit("10/minute")
async def analyze_ecosystem(request: Request):
    # Analysis logic here
    pass
```

#### **Input Validation**
```python
# backend/validation/schemas.py
from pydantic import BaseModel, validator

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v
```

---

## 📱 Mobile App Deployment

### **📲 React Native Deployment**

#### **Build for Android**
```bash
# Navigate to mobile app
cd EDIS_Mobile

# Install dependencies
npm install

# Android build
npx react-native build-android --mode=release

# Upload to Google Play Store
# Use Google Play Console
```

#### **Build for iOS**
```bash
# iOS build
npx react-native build-ios --mode=release

# Upload to App Store
# Use App Store Connect
```

---

## 🚀 Quick Deployment Checklist

### **✅ Pre-Deployment Checklist**
- [ ] **Environment variables** configured
- [ ] **SSL certificates** installed
- [ ] **Database** set up and migrated
- [ ] **API keys** secured and tested
- [ ] **Domain name** configured
- [ ] **Firewall rules** set
- [ ] **Backup strategy** implemented
- [ ] **Monitoring** configured
- [ ] **Error logging** enabled
- [ ] **Performance testing** completed

### **✅ Post-Deployment Checklist**
- [ ] **All endpoints** responding correctly
- [ ] **SSL certificate** valid
- [ ] **Database connections** working
- [ ] **Real-time features** functional
- [ ] **Mobile app** connecting
- [ ] **Monitoring alerts** configured
- [ ] **Backup restoration** tested
- [ ] **Load testing** passed
- [ ] **User acceptance** completed

---

## 💰 Cost Estimates

### **🏠 Local Deployment**
- **Hardware**: $0 (using existing computer)
- **Internet**: $20-50/month
- **Electricity**: $10-30/month
- **Total**: $30-80/month

### **☁️ Cloud Deployment**
- **Small Server**: $20/month (1-10 users)
- **Medium Server**: $50/month (10-50 users)
- **Large Server**: $200/month (50+ users)
- **Database**: $15-100/month
- **Domain & SSL**: $20/year
- **Total**: $50-400/month

### **🏢 Enterprise Deployment**
- **Load Balancer**: $50/month
- **Multiple Servers**: $200-2000/month
- **Database Cluster**: $100-500/month
- **CDN**: $50-200/month
- **Monitoring**: $100/month
- **Support Team**: $2000-10000/month
- **Total**: $2500-14000/month

---

## 🎯 Recommended Deployment Path

### **🚀 For Beginners**
1. **Start with local deployment** for testing
2. **Move to Vercel + Railway** for free hosting
3. **Upgrade to Docker + Cloud** as users grow

### **🏢 For Organizations**
1. **Start with Docker deployment** on cloud servers
2. **Add load balancing** for reliability
3. **Implement monitoring** and security
4. **Scale horizontally** as needed

---

## 📞 Support & Maintenance

### **🔧 Regular Maintenance**
- **Weekly**: Update dependencies, check logs
- **Monthly**: Security updates, performance optimization
- **Quarterly**: Backup testing, capacity planning
- **Annually**: Security audit, infrastructure review

### **🚨 Emergency Procedures**
- **Backup restoration**: 4-hour recovery time
- **Server failure**: Automatic failover
- **Security breach**: Incident response plan
- **Data corruption**: Point-in-time recovery

---

## 🌍 Conclusion

**Deploying EDIS for real-time use transforms it from a project into a production environmental monitoring platform.** 

Choose the deployment option that matches your:
- **Budget constraints**
- **Technical expertise**
- **User requirements**
- **Scalability needs**
- **Security requirements**

**Start simple, monitor performance, and scale as needed. Your EDIS can make a real impact on environmental monitoring and sustainability!**

---

## 📞 Deployment Support

For deployment assistance:
- **📧 Email**: deploy-support@edis.com
- **💬 Discord**: [EDIS Deployment Community](https://discord.gg/edis)
- **📚 Documentation**: [Full Deployment Guide](https://docs.edis.com/deployment)
- **🐛 Issues**: [GitHub Issues](https://github.com/edis/issues)

**🌍 Happy deploying! Your environmental intelligence platform awaits!**
