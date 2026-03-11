# 🌍 Earth Digital Immune System (EDIS)

## 📋 Problem Statement

**Environmental ecosystems are under unprecedented stress due to climate change, soil degradation, human pressure, and biodiversity loss.** 

Traditional environmental monitoring methods are often:
- 📍 **Location-specific** and limited in scope
- 📊 **Data-siloed** without integrated analysis
- 🤖 **Manual** and time-consuming
- 🌍 **Reactive** rather than predictive

**Monitoring ecosystem health is crucial** because:
- 🌡️ **Climate change** impacts food security and human health
- 🌱 **Soil degradation** affects agriculture and water quality
- 🦋 **Biodiversity loss** disrupts ecological balance
- 🏙️ **Human pressure** accelerates environmental degradation

---

## 🎯 Solution Overview

**Earth Digital Immune System (EDIS) is an AI-powered environmental intelligence platform** that monitors, analyzes, and predicts ecosystem health in real-time.

### **How EDIS Works**:
1. **🌍 Location Intelligence**: Converts any location to precise coordinates
2. **📊 Multi-Indicator Analysis**: Analyzes 5 key environmental indicators
3. **📈 Ecosystem Stress Index (ESI)**: Calculates comprehensive ecosystem health score
4. **🤖 AI-Powered Insights**: Generates environmental recommendations
5. **📊 Visual Intelligence**: Interactive maps and data visualizations
6. **🔮 Predictive Analytics**: Forecasts future ecosystem conditions

### **ESI Calculation Formula**:
```
ESI = (Climate Stress × 0.25) + 
       (Soil Health × 0.20) + 
       (Vegetation Cover × 0.20) + 
       (Human Pressure × 0.20) + 
       (Biodiversity Index × 0.15)
```

---

## ✨ Key Features

### **🔍 Ecosystem Analysis**
- **Real-time environmental monitoring** for any location
- **Professional command center dashboard** with live indicators
- **Comprehensive ESI calculation** with weighted scoring
- **Interactive data visualizations** (bar, radar, line charts)
- **AI environmental insights** with risk assessment
- **Downloadable environmental reports** in multiple formats

### **🗺️ Geo-AI Ecosystem Map**
- **Interactive India map** with 10+ major cities
- **Color-coded ecosystem health** indicators
- **Click-to-explore** detailed city environmental data
- **Real-time stress visualization** across regions
- **Geospatial analysis** of environmental patterns

### **🤖 AI Environmental Assistant**
- **Intelligent chat interface** for environmental queries
- **Context-aware responses** based on ecosystem data
- **Environmental recommendations** and restoration advice
- **Groq-powered LLaMA models** for advanced AI
- **Fallback intelligence** when API is unavailable

### **🎮 Scenario Simulator**
- **Interactive environmental modeling** and simulation
- **What-if analysis** for ecosystem changes
- **Impact assessment** of environmental interventions
- **Real-time visualization** of scenario outcomes
- **Educational tool** for environmental understanding

### **🔮 Future Ecosystem Predictor**
- **Machine learning predictions** for ecosystem health
- **6-year historical trend analysis** (2019-2024)
- **Future forecasting** with confidence intervals
- **Risk assessment** for environmental planning
- **Predictive analytics** for policy decisions


### **📄 Environmental Report Generator**
- **Comprehensive environmental reports** in PDF/text format
- **Executive summaries** for decision-makers
- **Technical appendices** for researchers
- **Actionable recommendations** for stakeholders
- **Automated report generation** with one click

---

## 🔄 How System Works

### **User Workflow**:
1. **📍 Enter Location** → User inputs city name or coordinates
2. **🌍 Geocoding** → System converts location to precise coordinates
3. **📊 Environmental Analysis** → 5 indicators are analyzed using ML models
4. **📈 ESI Calculation** → Weighted ecosystem stress index is computed
5. **📊 Visualization** → Interactive charts and maps display results
6. **🤖 AI Insights** → Assistant generates environmental recommendations
7. **📄 Report Generation** → Comprehensive environmental report is created

### **Technical Flow**:
```
User Input → Geocoding API → ML Models → ESI Calculator → 
Visualization Engine → AI Assistant → Report Generator
```

---

## 🛠️ Technology Stack

### **Frontend Technologies**
- **React.js** - Modern component-based UI framework
- **Framer Motion** - Smooth animations and transitions
- **CSS3** - Professional styling with responsive design
- **SVG/Canvas** - Interactive data visualizations

### **Backend Technologies**
- **FastAPI** - High-performance API framework
- **Python** - Core backend language
- **Uvicorn** - ASGI server for production deployment
- **CORS** - Cross-origin resource sharing

### **Machine Learning**
- **Scikit-learn** - ML model training and prediction
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing and array operations
- **Joblib** - Model serialization and loading

### **AI & Intelligence**
- **Groq API** - LLaMA models for AI assistant
- **Custom LLM Integration** - Flexible AI model support

### **Data & Visualization**
- **Chart.js** - Interactive data charts
- **OpenStreetMap** - Geocoding and mapping
- **Custom SVG** - Custom visualizations
- **HTML5 Canvas** - Advanced graphics rendering

---

## 📁 Project Structure

```
EDIS/
├── 📂 EDIS1/                    # Backend Services
│   ├── 📂 backend/              # API and business logic
│   │   ├── 📂 api/            # API routes and endpoints
│   │   ├── 📂 app/            # FastAPI application
│   │   ├── 📂 core/           # ML models and analysis
│   │   ├── 📂 services/       # Business logic services
│   │   └── 📂 edis_assistant/ # AI assistant logic
│   ├── 📂 data/               # Environmental datasets
│   └── 📂 ml/                # Machine learning models
└── 📂 EDIS_/                   # Frontend Application
    └── 📂 edis-dashboard/      # React frontend
        ├── 📂 src/
        │   ├── 📂 components/   # React components
        │   ├── 📂 pages/       # Page components
        │   └── 📂 styles/      # CSS styling
        └── 📂 public/          # Static assets
```

---

## 🌍 Live Demo

**🚀 Deployed Application**: [https://edis.vercel.app](https://edis.vercel.app)

**📊 Backend API**: [https://edis-backend.onrender.com](https://edis-backend.onrender.com)

---

## 🚀 Deployment Instructions

### **Backend Deployment (Render)**
1. **Connect GitHub Repository** to [Render](https://render.com/)
2. **Select Repository**: `sanjanamali17/EDIS`
3. **Configure Service**:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - **Health Check**: `/health`
4. **Set Environment Variables**:
   - `GROQ_API_KEY`: Your Groq API key
   - `DEBUG`: `false`
5. **Deploy**: Click "Create Web Service"

### **Frontend Deployment (Vercel)**
1. **Connect GitHub Repository** to [Vercel](https://vercel.com/)
2. **Import Repository**: `sanjanamali17/EDIS`
3. **Configure Build**:
   - **Framework**: Vite
   - **Root Directory**: `EDIS_/edis-dashboard`
   - **Build Command**: `npm install && npm run build`
   - **Output Directory**: `dist`
4. **Set Environment Variables**:
   - `VITE_API_URL`: `https://edis-backend.onrender.com/api`
5. **Deploy**: Click "Deploy"

### **Environment Variables Required**
```bash
# Backend (Render)
GROQ_API_KEY=your_groq_api_key
DEBUG=false

# Frontend (Vercel)
VITE_API_URL=https://edis-backend.onrender.com/api
```

---

## 💡 Example Usage

### **1. Ecosystem Analysis**
```bash
# User enters location: "Hyderabad"
# System automatically geocodes to: 17.3850°N, 78.4867°E
# Results displayed:
📍 Location: Hyderabad
📊 ESI: 40.1% (Moderate Stress)
🌡️ Climate Stress: 45.2%
🌱 Soil Health: 38.7%
🌿 Vegetation Cover: 35.2%
🏙️ Human Pressure: 51.3%
🦋 Biodiversity Index: 29.8%
```

### **2. Interactive Map**
```bash
# User clicks on Delhi marker
# Popup displays:
📍 Delhi: ESI 56.2% (High Stress)
📊 All environmental indicators
🎯 Risk assessment
💡 AI recommendations
```

### **3. AI Assistant**
```bash
# User asks: "What are the main environmental risks for Mumbai?"
# AI responds with:
🌊 Rising sea levels and coastal erosion
🌡️ Increasing temperature and heat waves
🏙️ Urban air pollution
💧 Water scarcity challenges
🌿 Loss of mangrove ecosystems
```

### **4. Report Generation**
```bash
# User clicks "Download Environmental Report"
# Generated report includes:
📋 Executive summary
📊 Environmental indicators
📈 Historical trends
🤖 AI insights and recommendations
🎯 Action plan for stakeholders
```

---

## 🚀 Future Improvements

### **🛰️ Satellite Data Integration**
- **Real-time satellite imagery** for live monitoring
- **NASA/ESA data feeds** for global coverage
- **Advanced remote sensing** for detailed analysis
- **Time-series satellite data** for trend analysis

### **⚡ Real-time Environmental Monitoring**
- **IoT sensor integration** for live data collection
- **Weather API integration** for current conditions
- **Air quality monitoring** stations integration
- **Water quality sensors** for river systems

### **🧠 Advanced Machine Learning**
- **Deep learning models** for better predictions
- **Neural networks** for complex pattern recognition
- **Ensemble methods** for improved accuracy
- **Transfer learning** for new regions

### **🌐 Global Expansion**
- **International city coverage** expansion
- **Multi-language support** for global users
- **Regional ecosystem models** for different biomes
- **Cross-border environmental analysis**

### **📱 Mobile Application**
- **React Native mobile app** for field use
- **Offline capabilities** for remote areas
- **Push notifications** for environmental alerts
- **GPS integration** for location-based analysis

---

## 🌍 Impact & Vision

**EDIS aims to democratize environmental intelligence** by providing:
- **Accessible tools** for environmental monitoring
- **Actionable insights** for sustainable development
- **Predictive capabilities** for proactive management
- **Educational resources** for environmental awareness

**Together, we can build a more sustainable future through intelligent environmental monitoring and management.**

---

## 📞 Contact & Support

- **📧 Email**: edis-support@example.com
- **🌐 Website**: https://edis-earth.com
- **📚 Documentation**: [Project Guide](./PROJECT_GUIDE.md)
- **🐛 Issues**: [GitHub Issues](https://github.com/edis/issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🌍 Earth Digital Immune System - Protecting Our Planet Through Intelligence**
