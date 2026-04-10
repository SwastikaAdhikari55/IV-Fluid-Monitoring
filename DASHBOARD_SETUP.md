# IV Monitoring System - Dashboard Setup Guide

## Overview
This is a responsive web dashboard for the AI IV Monitoring System. It's a single-page application (SPA) that communicates with the FastAPI backend via REST API.

## Quick Start

### 1. **Backend Setup**
The system uses a FastAPI backend that must be running for the dashboard to work.

```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend
python app.py
# or
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at: `http://localhost:8000`

### 2. **Frontend Setup**
Simply open the dashboard in a web browser:

```bash
# Option 1: Open directly in browser
open dashboard.html
# or navigate to: file:///path/to/dashboard.html

# Option 2: Use a local web server (recommended)
python -m http.server 8080
# Then open: http://localhost:8080/dashboard.html
```

## API Endpoints

The dashboard communicates with these FastAPI endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/data` | GET | Current IV level & drip rate |
| `/prediction` | GET | AI-powered finish time prediction |
| `/alerts` | GET | List of active alerts |
| `/alerts/{id}/acknowledge` | POST | Acknowledge a specific alert |
| `/alerts/reset` | POST | Clear all alerts |
| `/sensor-data` | POST | Receive IoT sensor data |
| `/dashboard` | GET | Complete dashboard status |
| `/health` | GET | Health check |

## Dashboard Features

### 1. **Real-time Monitoring**
- Updates every 2 seconds
- Live progress bars for IV level
- Drip rate monitoring
- System status indicators

### 2. **AI Predictions**
- Estimated IV finish time
- Confidence scores
- Minutes remaining calculation

### 3. **Alert System**
- Critical alerts (red) - IV level below 20%
- Warning alerts (yellow) - IV level below 40%
- Info alerts (blue) - System events
- One-click acknowledgment
- Alert timestamps

### 4. **Charts & Analytics**
- IV Level history (last 30 readings)
- Drip Rate history (last 30 readings)
- Real-time updates without page reload

### 5. **Device Status**
- Sensor connection indicator
- WiFi signal strength
- Battery level
- Color-coded status dots

### 6. **Patient Information**
- Patient name
- Bed number
- Bottle capacity
- Start time

### 7. **Responsive Design**
- Works on desktop, tablet, and mobile
- Sidebar collapses on mobile
- Touch-friendly controls
- Smooth animations

## Configuration

Edit the dashboard configuration in the JavaScript section:

```javascript
const CONFIG = {
    API_URL: 'http://localhost:8000',  // Change if backend is on different port
    DEVICE_ID: 'device_001',            // Device identifier
    REFRESH_INTERVAL: 2000,             // Update interval in milliseconds
    CHART_HISTORY: 30,                  // Number of data points in charts
    ALERT_THRESHOLD: 20,                // IV level alert threshold (%)
};
```

## Controls

### Buttons
- **Start Monitoring** - Begin live updates
- **Stop Monitoring** - Pause updates
- **Reset Alerts** - Clear all active alerts

### Navigation
- **Dashboard** - Main monitoring view
- **Patients** - Patient management (placeholder)
- **Alerts** - Alert history (clickable)
- **Settings** - System configuration (clickable)

## Color Coding

### Status Indicators
- 🟢 **Green** - Normal operation
- 🟡 **Yellow** - Warning (low IV level)
- 🔴 **Red** - Critical (very low IV level)

### Alert Types
- **Critical** (Red) - Requires immediate attention
- **Warning** (Yellow) - Monitor closely
- **Info** (Blue) - Informational events

## Troubleshooting

### Dashboard Won't Connect
1. Check backend is running: `http://localhost:8000/health`
2. Verify API_URL in dashboard matches backend address
3. Check browser console for errors (F12)
4. Ensure CORS is enabled in FastAPI backend

### No Data Appearing
1. Click "Start Monitoring" button
2. Check API endpoint `/data` is working
3. Verify backend has sensor data

### Charts Not Displaying
1. Ensure Chart.js CDN is accessible
2. Check browser console for JavaScript errors
3. Wait for first data points (takes ~2 seconds)

## Browser Support
- Chrome/Edge 80+
- Firefox 75+
- Safari 13+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Notes
- Responsive updates: 2-second refresh interval
- Chart history: Limited to 30 data points (configurable)
- Smooth animations: 60fps target
- Mobile-optimized: Touch-friendly UI

## Security Considerations
1. Use HTTPS in production
2. Implement authentication for API endpoints
3. Add rate limiting to prevent abuse
4. Validate all user inputs
5. Use environment variables for sensitive config

## Advanced Features

### Custom Backend Port
Update CONFIG.API_URL:
```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000',  // Your port
    // ... rest of config
};
```

### Auto-start Monitoring
Uncomment this line in initialization:
```javascript
// Auto-start monitoring (optional)
startMonitoring();
```

### Modify Refresh Interval
```javascript
const CONFIG = {
    REFRESH_INTERVAL: 1000,  // 1 second
    // or
    REFRESH_INTERVAL: 5000,  // 5 seconds
};
```

## File Structure
```
/
├── dashboard.html          # Main single-page dashboard
├── app.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── models.py              # Database models
├── sensor_service.py      # Sensor data handling
├── alert_service.py       # Alert management
├── prediction_service.py  # AI prediction engine
└── README.md              # This file
```

## Development

### Testing the API
Use the provided test script:
```bash
python test_api.py
```

### Simulating Sensor Data
Make a POST request to test alert generation:
```bash
curl -X POST http://localhost:8000/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device_001",
    "iv_level": 25,
    "drip_rate": 35,
    "temperature": 22.5
  }'
```

## Support & Issues
If you encounter issues:
1. Check the browser console (F12)
2. Verify backend is running
3. Check network tab for failed requests
4. Review API response format
5. Check logs: `tail -f backend.log`

---

**Version**: 1.0  
**Last Updated**: 2026-04-10  
**Status**: Production Ready
