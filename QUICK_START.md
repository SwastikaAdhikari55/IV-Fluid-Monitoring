# IV Monitoring System - Quick Start Guide

Get the production-ready IV monitoring backend running in **60 seconds**!

## 📋 Prerequisites

- Python 3.9+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Terminal/Command Prompt

## 🚀 Three Steps to Success

### Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

### Step 2: Start Backend (10 seconds)

```bash
python start.py
```

**You should see:**
```
╔════════════════════════════════════════════════════════════╗
║  IV MONITORING SYSTEM - BACKEND STARTING                  ║
╚════════════════════════════════════════════════════════════╝

✓ Backend server running at http://localhost:8000
✓ API Documentation: http://localhost:8000/docs
✓ Alternative Docs: http://localhost:8000/redoc
```

### Step 3: Test the Backend (10 seconds)

Open **new terminal** and run:

```bash
python test_api.py
```

---

## 🌐 Access API

Open browser to: **http://localhost:8000/docs**

This gives you interactive Swagger UI to test all endpoints!

---

## 📡 Quick API Tests
```
File → Open → dashboard.html
```

**Option B: Local Web Server (Recommended)**
```bash
# Terminal 1 is running the backend (from Step 2)

# Terminal 2 - Start web server
python -m http.server 8080

# Then open browser to:
http://localhost:8080/dashboard.html
```

**Option C: VS Code Live Server**
- Right-click dashboard.html → "Open with Live Server"

## ✅ Verify Everything Works

### Check Backend
```bash
# In a new terminal
curl http://localhost:8000/health

# Expected response:
# {"status":"ok","timestamp":"...","device":"device_001"}
```

### Test API Endpoints
```bash
# Run comprehensive test suite
python test_dashboard.py
```

### Check Browser Console
Open browser DevTools (F12 → Console) - should show:
```
✓ Dashboard initialized
✓ Charts loaded
✓ Fetching data from http://localhost:8000/data
```

## 📊 Dashboard Overview

### Main Components

```
┌─────────────────────────────────────────────────────────────┐
│    💉 AI IV Monitoring System                               │
└─────────────────────────────────────────────────────────────┘
┌──────────────┬─────────────────────────────────────────────┐
│ SIDEBAR      │  CONTENT AREA                               │
│              │  ┌──────────┬──────────┬──────────┐         │
│ Dashboard    │  │ IV Level │ Drip Rt  │ Status   │         │
│ Patients     │  └──────────┴──────────┴──────────┘         │
│ Alerts       │  ┌──────────┬──────────────────────┐         │
│ Settings     │  │ Finish Tm │ Patient Info Panel   │         │
│              │  └──────────┴──────────────────────┘         │
│              │  ┌────────────────────────────────┐          │
│              │  │ Active Alerts Panel             │         │
│              │  └────────────────────────────────┘         │
│              │  ┌────────────┬────────────┐                 │
│              │  │ IV Chart   │ Drip Chart │                 │
│              │  └────────────┴────────────┘                 │
│              │  [Start] [Stop] [Reset Alerts]               │
└──────────────┴─────────────────────────────────────────────┘
```

### Key Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Real-time Updates | ✓ | Updates every 2 seconds |
| IV Level Progress | ✓ | Visual percentage bar |
| Drip Rate Monitor | ✓ | Drops per minute |
| AI Predictions | ✓ | Estimated finish time |
| Alert System | ✓ | Critical/Warning/Info |
| Charts | ✓ | 30-point history |
| Device Status | ✓ | Sensor, WiFi, Battery |
| Patient Info | ✓ | Name, Bed, Capacity |
| Responsive Design | ✓ | Mobile, Tablet, Desktop |

## 🎮 Using the Dashboard

### Start Monitoring
1. Click **"▶️ Start Monitoring"** button
2. Dashboard starts fetching live data
3. Charts begin populating
4. Status updates in real-time

### Stop Monitoring
1. Click **"⏹️ Stop Monitoring"** button
2. Updates pause (data stays on screen)
3. Can restart anytime

### View Alerts
- Active alerts appear in **Alert Panel**
- Color coded: 🔴 Critical, 🟡 Warning, 🔵 Info
- Click **"Acknowledge"** to mark alert as handled

### Reset Alerts
- Click **"🔄 Reset Alerts"** button
- Clears all active alerts
- System continues monitoring

### Navigate Pages
- **Dashboard** - Main monitoring view
- **Patients** - Patient management (expandable)
- **Alerts** - Alert history view
- **Settings** - System configuration

## 🔧 Configuration

Edit dashboard settings in `dashboard.html` (around line 450):

```javascript
const CONFIG = {
    API_URL: 'http://localhost:8000',    // Backend URL
    DEVICE_ID: 'device_001',              // Device ID
    REFRESH_INTERVAL: 2000,               // Update interval (ms)
    CHART_HISTORY: 30,                    // Chart data points
    ALERT_THRESHOLD: 20,                  // Alert threshold (%)
};
```

|** Setting** | **Default** | **Unit** | **Notes** |
|-----------|---------|------|-------|
| API_URL | localhost:8000 | URL | Change if backend on different port |
| DEVICE_ID | device_001 | - | Unique device identifier |
| REFRESH_INTERVAL | 2000 | ms | Lower = more frequent updates (min 500ms) |
| CHART_HISTORY | 30 | points | More points = better history but slower |
| ALERT_THRESHOLD | 20 | % | IV level below this triggers critical alert |

## 🌐 API Endpoints Reference

```
GET  /health                           Health check
GET  /data                             Current IV & drip rate
GET  /prediction                       Estimated finish time
GET  /alerts                           List active alerts
GET  /dashboard                        Complete dashboard data
GET  /history                          Historical chart data
GET  /device-info                      Device information

POST /sensor-data                      Send sensor reading
POST /alerts/{id}/acknowledge          Acknowledge alert
POST /alerts/reset                     Clear all alerts
POST /test-alert                       Generate test alert
```

### Example API Calls

```bash
# Get current data
curl http://localhost:8000/data

# Get prediction
curl http://localhost:8000/prediction

# Get alerts
curl http://localhost:8000/alerts

# Send sensor data
curl -X POST http://localhost:8000/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device_001",
    "iv_level": 75.5,
    "drip_rate": 45.2,
    "temperature": 22.5
  }'

# Acknowledge alert
curl -X POST http://localhost:8000/alerts/1/acknowledge

# Reset all alerts
curl -X POST http://localhost:8000/alerts/reset
```

## 🎨 Visual Design

### Color Scheme
- **Primary**: Blue (`#667eea`)
- **Secondary**: Purple (`#764ba2`)
- **Success**: Green (`#4CAF50`)
- **Warning**: Yellow (`#FFC107`)
- **Critical**: Red (`#f44336`)

### Theme Elements
- Rounded cards with soft shadows
- Medical dashboard aesthetic
- Smooth animations & transitions
- Gradient backgrounds
- Clean typography

## 📱 Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Desktop | > 1024px | Sidebar left, full grid |
| Tablet | 768px - 1024px | Sidebar top, 2-col grid |
| Mobile | < 768px | Sidebar top, 1-col grid |

## 🐛 Troubleshooting

### "Cannot connect to API"
```bash
# Check if backend is running
curl http://localhost:8000/health

# If error, start backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### "Charts not showing"
1. Open DevTools (F12)
2. Check Console for errors
3. Verify Chart.js CDN is accessible
4. Wait 2-3 seconds for data to populate

### "No data updates"
1. Click "Start Monitoring" button
2. Check `/data` endpoint: `curl http://localhost:8000/data`
3. Verify backend has sensor data

### "Alerts not appearing"
1. Verify backend is generating alerts
2. Check Alert System logs
3. Ensure IV level is below threshold (default 20%)

### Dashboard loads but is blank
1. Check browser console for JavaScript errors
2. Verify API URL is correct
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try different browser

## 📚 Additional Resources

- **Full Documentation**: See `DASHBOARD_SETUP.md`
- **Backend Setup**: See `STARTUP.md`
- **API Integration Examples**: See `FRONTEND_EXAMPLES.md`
- **Project Guide**: See `GUIDE.md`

## 🔐 Production Deployment

### Security Checklist
- [ ] Change default API URLs
- [ ] Enable HTTPS/TLS
- [ ] Set up authentication
- [ ] Enable CORS properly
- [ ] Add request rate limiting
- [ ] Use environment variables for secrets
- [ ] Implement API key validation
- [ ] Add input validation
- [ ] Set up logging & monitoring
- [ ] Use secure database

### Performance Tuning
```javascript
// Increase interval for slower networks
REFRESH_INTERVAL: 5000,  // 5 seconds

// Reduce chart history
CHART_HISTORY: 15,  // Fewer points

// Adjust for production
DEBUG_MODE: false,
```

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review DASHBOARD_SETUP.md
3. Check browser console (F12)
4. Run test_dashboard.py
5. Review FastAPI logs
6. Check sensor_service.py for data generation

## ✨ Best Practices

1. **Performance**
   - Use REFRESH_INTERVAL >= 1000ms
   - Keep CHART_HISTORY under 50
   - Use web server for frontend

2. **Monitoring**
   - Start monitoring before viewing data
   - Check device status indicators
   - Review alerts regularly

3. **Data**
   - Ensure sensor inputs are valid
   - Validate API responses
   - Monitor network requests

4. **Maintenance**
   - Keep dependencies updated
   - Review logs regularly
   - Test alerts frequently

---

**Last Updated**: 2026-04-10  
**Version**: 1.0  
**Status**: ✅ Production Ready

Need help? Check the DevTools console or run `test_dashboard.py`!
