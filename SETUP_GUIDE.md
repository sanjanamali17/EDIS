# 🌍 Earth Digital Immune System (EDIS)

# 📘 Project Setup & Usage Guide

---

## 📌 1. Introduction

Earth Digital Immune System (EDIS) is an AI-powered environmental intelligence platform that analyzes ecosystem health, predicts future risks, and provides actionable insights.

This guide explains how to set up and run the project from scratch.

---

## 🛠 2. System Requirements

Make sure you have the following installed:

### 🔹 Software Requirements

- **Python** (>= 3.9)
- **Node.js** (>= 16)
- **npm** 
- **Git**

### 🔹 Recommended Tools

- **VS Code**
- **Postman** or **swagger ui** (for API testing)

---

## 📦 3. Project Structure

```
EDIS/
├── EDIS1/                    # Backend services
│   └── backend/              # FastAPI application
│       ├── api/              # API endpoints
│       ├── core/             # ML models
│       ├── services/         # Business logic
│       ├── edis_assistant/   # AI assistant
│       └── data/            # Datasets
├── EDIS_/                   # Frontend application
│   └── edis-dashboard/       # React application
│       ├── src/              # Source code
│       ├── public/           # Static assets
│       └── package.json     # Dependencies
├── EDIS_COMPREHENSIVE_DOCUMENTATION.md  # Technical docs
├── PROJECT_GUIDE.md                  # Project overview
└── README.md                        # Project summary
```

---

## ⚙️ 4. Backend Setup (FastAPI)

### Step 1: Navigate to backend
```bash
cd EDIS1/backend
```

### Step 2: Create virtual environment
```bash
python -m venv venv
```

### Step 3: Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run backend server
```bash
python start_server.py
```

**Backend will run at:**
```
http://127.0.0.1:8000
```

---

## 💻 5. Frontend Setup (React)

### Step 1: Navigate to frontend
```bash
cd EDIS_/edis-dashboard
```

### Step 2: Install dependencies
```bash
npm install
```

### Step 3: Run frontend
```bash
npm run dev
```

**Frontend will run at:**
```
http://localhost:5173
```

---

## 🔗 6. Connecting Frontend & Backend

Make sure your frontend API URL points to backend:

**Example:**
```javascript
const API_URL = "http://127.0.0.1:8000";
```

---

## 📊 7. How to Use the Project

### 1. Open frontend in browser
Navigate to `http://localhost:5173`

### 2. Enter a location (city or coordinates)
Examples: "Hyderabad", "Delhi", "19.0760,72.8777"

### 3. Click on "Analyze"
This will:
- Fetch environmental indicators
- Calculate Ecosystem Stress Index (ESI)
- Generate AI insights
- Display charts and visualizations

### 4. View Results:
- **Ecosystem Stress Index (ESI)** - Overall ecosystem health score
- **Environmental Indicators** - Individual stress factors
- **Charts & Graphs** - Visual representation of data
- **AI Insights** - Environmental recommendations

### 5. Navigate to other features:
- **AI Assistant** - Chat with environmental AI
- **Future Predictor** - Predict ecosystem changes
- **Map** - Interactive ecosystem intelligence map

---

## 🤖 8. AI Assistant

The EDIS Assistant provides:
- **Environmental Q&A** - Ask questions about ecosystem health
- **Risk Analysis** - Get insights on environmental threats
- **Recommendations** - Receive actionable advice
- **Educational Content** - Learn about environmental science

**Example Questions:**
- "What are the main environmental risks in this area?"
- "How can we improve soil health?"
- "What's the biodiversity status here?"

---

## 🔮 9. Future Predictor

The Future Ecosystem Predictor:
- **Select Location** - Choose any city or coordinates
- **View Predictions** - See 5-year ecosystem forecasts
- **Analyze Trends** - Understand environmental changes
- **Risk Assessment** - Identify future environmental risks

**Features:**
- Time-series predictions
- Confidence intervals
- Scenario analysis
- Historical trend comparison

---

## 🗺️ 10. Interactive Map

The Ecosystem Intelligence Map:
- **Interactive Visualization** - Click on cities for details
- **Color-Coded Health** - Green (healthy) to Red (high stress)
- **Real-time Data** - Current ecosystem conditions
- **Detailed Popups** - Comprehensive environmental information

---

## ⚠️ 11. Common Issues & Fixes

### Issue: Backend not running

**✅ Check if virtual environment is activated**
```bash
# Check for (venv) prefix in terminal
which python
```

**✅ Ensure dependencies are installed**
```bash
pip list | grep fastapi
```

### Issue: Frontend not connecting to backend

**✅ Check API URL**
- Verify API_URL in `src/api.js`
- Ensure backend is running on correct port

**✅ Check CORS settings**
- Backend should have CORS enabled
- Frontend URL should be allowed

### Issue: Port already in use

**✅ Change port:**
```bash
# Backend
uvicorn main:app --port 8001

# Frontend (edit package.json)
"scripts": {
  "dev": "vite --port 3000"
}
```

### Issue: Missing dependencies

**✅ Install missing packages:**
```bash
# Backend
pip install fastapi uvicorn pandas numpy scikit-learn

# Frontend
npm install axios chart.js react-chartjs-2 framer-motion
```

---

## 📦 12. Installed Packages

### Backend Dependencies

```txt
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
requests==2.31.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.13.6",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "framer-motion": "^10.16.0",
    "leaflet": "^1.9.4",
    "react-leaflet": "^4.2.1",
    "react-icons": "^4.12.0",
    "react-markdown": "^10.1.0",
    "recharts": "^3.8.0"
  }
}
```

---

## 🚀 13. Deployment (Optional)

### Backend Deployment Options:
- **Render** - Easy Python deployment
- **Heroku** - Platform as a Service
- **AWS Lambda** - Serverless functions
- **DigitalOcean** - Cloud servers

**Build for Production:**
```bash
# Frontend
cd EDIS_frontend/edis-dashboard
npm run build

# Backend
cd EDIS1/backend
pip install gunicorn
```

---

## 🧑‍💻 14. Developer Notes

### Best Practices:
- **Ensure consistent data flow** between backend and frontend
- **Avoid hardcoding values** - use environment variables
- **Maintain clean UI** - follow design patterns
- **Test API endpoints** before frontend integration
- **Use proper error handling** for robust applications

### Code Organization:
- **Modular components** - Reusable and maintainable
- **Clear naming** - Descriptive variable and function names
- **Documentation** - Comment complex logic
- **Version control** - Regular commits with clear messages

### Performance Tips:
- **Lazy loading** for large components
- **API caching** for frequently accessed data
- **Image optimization** for faster loading
- **Bundle size optimization** for frontend

---

## 🌍 15. Environmental Impact

### EDIS Supports:
- **SDG 13** - Climate Action
- **SDG 15** - Life on Land
- **SDG 6** - Clean Water and Sanitation
- **SDG 11** - Sustainable Cities
- **SDG 7** - Clean Energy

### Real-World Applications:
- **Urban Planning** - Sustainable city development
- **Agriculture** - Soil health and crop management
- **Conservation** - Biodiversity protection
- **Policy Making** - Data-driven environmental decisions
- **Education** - Environmental awareness and learning

---

## 🔬 16. Technical Architecture

### Data Flow:
```
User Input → Frontend → API → ML Models → AI Assistant → Visualization → User
```

### Key Components:
- **Environmental Indicators** - 5 core metrics
- **ESI Calculation** - Weighted scoring algorithm
- **Machine Learning** - Prediction and analysis
- **AI Assistant** - Natural language processing
- **Visualization** - Charts and interactive maps

### API Endpoints:
```
POST /api/analyze/climate          - Climate stress analysis
POST /api/analyze/soil            - Soil health evaluation
POST /api/analyze/vegetation       - Vegetation analysis
POST /api/analyze/human             - Human pressure assessment
POST /api/analyze/biodiversity      - Biodiversity calculation
POST /api/edis/chat                - AI assistant
GET  /api/predict/ecosystem         - Future predictions
```

---

## 🌟 17. Future Enhancements

### Planned Features:
- **Real-time Data Streaming** - Live environmental monitoring
- **Mobile Application** - Field data collection
- **Global Coverage** - International cities and ecosystems
- **Advanced AI** - Multi-modal environmental analysis
- **Collaborative Tools** - Team-based analysis
- **API Integration** - Third-party data sources

### Technical Improvements:
- **Microservices Architecture** - Scalable system design
- **Cloud Deployment** - Global accessibility
- **Advanced ML Models** - Improved prediction accuracy
- **Real-time Alerts** - Environmental threat notifications
- **Data Visualization** - 3D and interactive charts

---

## 🌍 18. Conclusion

Earth Digital Immune System (EDIS) demonstrates how AI and machine learning can be used for:

- **Environmental Monitoring** - Real-time ecosystem health tracking
- **Predictive Analysis** - Future environmental risk assessment
- **Decision Support** - Data-driven environmental management
- **Education & Awareness** - Environmental science learning
- **Sustainable Development** - Supporting global environmental goals

---

## 🎯 Final Note

If you follow this guide step by step, the project will run successfully without issues. The system provides a comprehensive platform for environmental intelligence and sustainable development planning.

---

## 📞 Support & Resources

### 📚 Additional Documentation:
- **EDIS_COMPREHENSIVE_DOCUMENTATION.md** - Complete technical documentation
- **PROJECT_GUIDE.md** - Project overview and architecture
- **README.md** - Quick start guide

### 🤝 Contributing:
- Fork the repository
- Create feature branches
- Submit pull requests
- Participate in code reviews

### 🌐 Online Resources:
- **GitHub Repository** - Source code and issues
- **API Documentation** - Interactive API docs
- **Community Forum** - Developer discussions

---

**🌍 Earth Digital Immune System - Environmental Intelligence for a Sustainable Future**

*This guide provides everything needed to set up, run, and contribute to the EDIS platform. Together, we can build a more sustainable future through intelligent environmental monitoring and management.*
