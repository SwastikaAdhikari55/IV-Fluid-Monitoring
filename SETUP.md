# IV Monitoring System - Complete Setup & Run Guide

## 📋 Prerequisites

- **Python 3.9+** 
- **pip** (Python package manager)
- **Terminal/Command Prompt**

---

## 🚀 Step 1: Install Dependencies

Run this command once to install all required packages:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- WebSockets - Real-time communication
- And other dependencies

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 ...
```

---

## 🏃 Step 2: Start the Backend Server

### Option A: Quick Start (Recommended)
```bash
python start.py
```

This script will:
- ✓ Check Python version
- ✓ Verify all dependencies
- ✓ Create `.env` file if needed
- ✓ Initialize SQLite database
- ✓ Start the FastAPI server

### Option B: Direct Start
```bash
python app.py
```

---

## ✅ Verify It's Running

You should see output like:

```
╔════════════════════════════════════════════════════════════╗
║  IV MONITORING SYSTEM - BACKEND STARTING                  ║
╚════════════════════════════════════════════════════════════╝

✓ Backend server running at http://localhost:8000
✓ API Documentation: http://localhost:8000/docs
✓ Alternative Docs: http://localhost:8000/redoc
```

**The server is ready when you see this!**

---

## 🔍 Test the API

### Open Interactive Documentation

While the server is running, open your browser and go to:

**http://localhost:8000/docs**

This shows the Swagger UI with all endpoints. You can test any endpoint directly here!

---

## 🧪 Run Full Test Suite

Open a **NEW TERMINAL** (keep the server running in the original) and run:

```bash
python test_api.py
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════╗
║  IV MONITORING SYSTEM - API TEST SUITE                    ║
╚════════════════════════════════════════════════════════════╝

⚠️  Make sure the backend is running: python app.py

Press Enter to start tests...
```

Press Enter to run all tests. Expected tests:
1. ✓ PASS: Health Check
2. ✓ PASS: Send Green Status Data
3. ✓ PASS: Send Yellow Status Data
4. ✓ PASS: Send Red Status Data (Alert)
5. ✓ PASS: Get Dashboard
6. ✓ PASS: Get Prediction
7. ✓ PASS: Get Alerts
8. ✓ PASS: Acknowledge Alert
9. ✓ PASS: Simulate Sensor Data
10. ✓ PASS: WebSocket Connection

---

## 📡 Quick API Examples

### 1. Send Sensor Data
```bash
curl -X POST http://localhost:8000/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device_001",
    "iv_level": 85.5,
    "drip_rate": 45.2,
    "temperature": 22.5
  }'
```

**Response:**
```json
{
  "success": true,
  "device_id": "device_001",
  "iv_level": 85.5,
  "drip_rate": 45.2,
  "status_color": "green",
  "timestamp": "2024-04-10T14:30:00.123456",
  "message": "Reading stored successfully. Status: GREEN"
}
```

### 2. Check Dashboard  
```bash
curl http://localhost:8000/dashboard?device_id=device_001
```

### 3. Get Prediction
```bash
curl http://localhost:8000/prediction?device_id=device_001
```

### 4. Get Alerts
```bash
curl http://localhost:8000/alerts
```

### 5. Generate Test Data
```bash
curl -X POST http://localhost:8000/simulate/device_001
```

---

## 🎯 Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/sensor-data` | Send IoT sensor reading |
| GET | `/dashboard` | Get device status |
| GET | `/prediction` | Get IV finish time prediction |
| GET | `/alerts` | Get active alerts |
| POST | `/alerts/{id}/acknowledge` | Mark alert as seen |
| DELETE | `/alerts/{id}` | Resolve alert |
| POST | `/simulate/{device_id}` | Generate test data |
| WS | `/ws/{device_id}` | Real-time WebSocket updates |

---

## 🐛 Troubleshooting

### Error: "Port 8000 already in use"
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>

# Or use different port:
PORT=8001 python app.py
```

### Error: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Error: "Database locked"
```bash
# Remove and recreate database
rm iv_monitoring.db
python start.py
```

### WebSocket tests fail
- Ensure backend is running
- Check firewall settings
- Try the Swagger UI to verify API is working

---

## 📁 Project Structure

```
IV-Fluid-Monitoring/
├── app.py                      # Main FastAPI application (830 lines)
├── models.py                   # SQLAlchemy ORM models
├── config.py                   # Configuration settings
├── sensor_service.py           # Sensor data ingestion logic
├── alert_service.py            # Alert threshold & notifications
├── prediction_service.py       # AI prediction engine
├── start.py                    # Quick start script
├── test_api.py                 # Comprehensive API tests
├── requirements.txt            # Python dependencies
├── iv_monitoring.db           # SQLite database (auto-created)
├── README.md                   # User documentation
├── GUIDE.md                    # Implementation guide
└── SETUP.md                    # This file
```

---

## 🔄 Typical Development Workflow

### Terminal 1: Run Backend
```bash
python start.py
# or: python app.py
```

### Terminal 2: Test API
```bash
# Option A: Run full test suite
python test_api.py

# Option B: Use curl for specific endpoints
curl http://localhost:8000/

# Option C: Open browser to Swagger UI
# http://localhost:8000/docs
```

---

## 📊 Database

The system uses **SQLite** by default (file: `iv_monitoring.db`).

### Tables automatically created:
1. **sensor_data** - IoT readings (IV level, drip rate)
2. **device_status** - Current status cache
3. **alerts** - Alert history and state
4. **predictions** - IV finish time predictions

### Query by device:
```python
# Get last 100 readings for device_001
SELECT * FROM sensor_data 
WHERE device_id = 'device_001' 
ORDER BY timestamp DESC 
LIMIT 100;
```

---

## 🚀 Production Deployment

To run on a different port:
```bash
PORT=3000 python app.py
```

To disable debug mode:
```bash
DEBUG=False python app.py
```

To use PostgreSQL (production database):
```bash
DATABASE_URL="postgresql://user:pass@localhost/iv_monitoring" python app.py
```

---

## 📞 Need Help?

### Check logs for errors:
- Watch terminal output while running `python app.py`
- Errors are printed with timestamps and details

### Verify endpoints:
- Open http://localhost:8000/docs
- Try endpoints directly in Swagger UI
- Read the documentation for each endpoint

### Run test suite:
```bash
python test_api.py
```

---

## ✨ Features Summary

✅ **Real-Time Monitoring** - Dashboard with live updates  
✅ **Smart Alerts** - CRITICAL (Red), WARNING (Yellow), INFO (Green)  
✅ **AI Predictions** - Estimates IV finish time with confidence score  
✅ **WebSocket Support** - Real-time push updates to clients  
✅ **IoT Integration** - Receives data from monitoring devices  
✅ **REST API** - Complete Swagger documentation  
✅ **Production Ready** - Error handling, logging, validation  
✅ **Database** - SQLite (dev) or PostgreSQL (production)  

---

**Ready to start? Run: `python start.py`**

