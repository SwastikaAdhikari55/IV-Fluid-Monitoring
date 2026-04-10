# IV Monitoring System - Backend

A production-ready REST API backend for real-time IV (Intravenous) fluid monitoring with AI-powered prediction, automated alerts, and real-time WebSocket support.

## 🎯 Features

✅ **Real-Time Monitoring** - Dashboard showing IV level and drip rate
✅ **Smart Status Indicators** - Green (>60%), Yellow (30-60%), Red (<30%)
✅ **Automated Alerts** - Mobile notifications + buzzer simulation
✅ **AI Predictions** - Estimates IV finish time using trend analysis
✅ **IoT Data Ingestion** - Receive sensor data via REST API
✅ **WebSocket Support** - Real-time updates without polling
✅ **Cloud-Ready** - SQLAlchemy ORM supports PostgreSQL
✅ **Production Architecture** - Clean separation of concerns, comprehensive logging

## 📋 Project Structure

```
iv-monitoring-system/
├── app.py                    # Main FastAPI application
├── config.py                 # Configuration settings
├── models.py                 # SQLAlchemy ORM models
├── sensor_service.py         # IoT sensor data handling
├── alert_service.py          # Alert management & notifications
├── prediction_service.py     # AI prediction logic
├── requirements.txt          # Python dependencies
├── iv_monitoring.db         # SQLite database (auto-created)
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Run the Backend**

```bash
python app.py
```

The API will start at: `http://localhost:8000`

### 3. **Access Interactive API Documentation**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Check
```
GET /
```
Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "IV Monitoring System",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### Receive Sensor Data
```
POST /sensor-data
```
Submit IoT sensor readings from IV monitoring devices.

**Request Body:**
```json
{
  "device_id": "device_001",
  "iv_level": 75.5,
  "drip_rate": 45.2,
  "temperature": 22.5
}
```

**Response:**
```json
{
  "success": true,
  "device_id": "device_001",
  "iv_level": 75.5,
  "drip_rate": 45.2,
  "status_color": "green",
  "timestamp": "2024-01-15T10:30:00.123456",
  "message": "Reading stored successfully. Status: GREEN"
}
```

**Status Colors:**
- 🟢 **GREEN** - IV level > 60% (safe)
- 🟡 **YELLOW** - IV level 30-60% (warning, refill soon)
- 🔴 **RED** - IV level < 30% (critical, refill immediately)

---

### Get Dashboard
```
GET /dashboard?device_id=device_001
```
Retrieve current status for device(s).

**Query Parameters:**
- `device_id` (optional) - Specific device to query

**Response:**
```json
[
  {
    "device_id": "device_001",
    "current_iv_level": 75.5,
    "current_drip_rate": 45.2,
    "status_color": "green",
    "last_reading_at": "2024-01-15T10:30:00",
    "active_alerts": 0,
    "prediction": {
      "estimated_finish_time": "2024-01-15T12:00:00",
      "minutes_remaining": 89.5,
      "confidence_score": 0.85,
      "based_on_readings": 15
    }
  }
]
```

---

### Get AI Prediction
```
GET /prediction?device_id=device_001
```
Request IV finish time prediction for a device.

**Query Parameters:**
- `device_id` (required) - Device to predict for

**Response:**
```json
{
  "device_id": "device_001",
  "estimated_finish_time": "2024-01-15T12:00:00",
  "minutes_remaining": 89.5,
  "confidence_score": 0.92,
  "based_on_readings": 25
}
```

**How Prediction Works:**
1. Current IV level ÷ Drip rate = Minutes remaining
2. Analyzes last 50 sensor readings for trends
3. Adjusts prediction based on drip rate patterns
4. Confidence increases with more historical data (0-1 scale)

---

### Get Active Alerts
```
GET /alerts?device_id=device_001
```
Retrieve all active and acknowledged alerts.

**Query Parameters:**
- `device_id` (optional) - Filter by specific device

**Response:**
```json
[
  {
    "id": 1,
    "device_id": "device_001",
    "alert_type": "critical",
    "iv_level": 25.0,
    "message": "CRITICAL: IV level critically low (25.0%)",
    "status": "active",
    "triggered_at": "2024-01-15T10:45:00",
    "acknowledged_at": null
  },
  {
    "id": 2,
    "device_id": "device_001",
    "alert_type": "warning",
    "iv_level": 45.0,
    "message": "WARNING: IV level low (45.0%)",
    "status": "acknowledged",
    "triggered_at": "2024-01-15T10:30:00",
    "acknowledged_at": "2024-01-15T10:32:00"
  }
]
```

---

### Acknowledge Alert
```
POST /alerts/{alert_id}/acknowledge
```
Mark an alert as acknowledged by staff.

**Response:**
```json
{
  "success": true,
  "message": "Alert acknowledged"
}
```

---

### Resolve Alert
```
DELETE /alerts/{alert_id}
```
Clear/resolve an alert.

**Response:**
```json
{
  "success": true,
  "message": "Alert resolved"
}
```

---

### Simulate Sensor Data (Testing)
```
POST /simulate/{device_id}
```
Generate realistic simulated sensor data (useful for demo/testing).

**Response:**
```json
{
  "success": true,
  "device_id": "device_001",
  "iv_level": 72.3,
  "drip_rate": 43.8,
  "status_color": "green",
  "timestamp": "2024-01-15T10:31:00.234567",
  "message": "Reading stored successfully. Status: GREEN"
}
```

---

## 🔄 WebSocket Real-Time Updates

Connect to WebSocket for real-time dashboard updates (no polling needed).

**Connection URL:**
```
ws://localhost:8000/ws/{device_id}
```

**Example (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/device_001');

ws.onopen = () => {
  console.log('Connected to IV monitoring');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update received:', data);
  // Update dashboard in real-time
  updateDashboard(data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

**Message Types:**
```json
// Sensor update
{
  "type": "sensor_update",
  "device_id": "device_001",
  "iv_level": 75.5,
  "drip_rate": 45.2,
  "status_color": "green",
  "timestamp": "2024-01-15T10:30:00"
}

// Simulated update
{
  "type": "simulated_update",
  "device_id": "device_001",
  "iv_level": 72.3,
  "drip_rate": 43.8,
  "status_color": "green"
}
```

## 📊 Alert System

### Alert Types & Thresholds

| Status | Type | Threshold | Action |
|--------|------|-----------|--------|
| 🟢 Green | Info | IV > 60% | Monitor only |
| 🟡 Yellow | Warning | 30% ≤ IV ≤ 60% | Staff notification |
| 🔴 Red | Critical | IV < 30% | Mobile alert + Buzzer |

### Alert Lifecycle

```
┌─────────────────────────────────────┐
│  Alert Triggered (IV < 30%)         │
│  - Mobile notification sent         │
│  - Buzzer simulation triggered      │
│  - Status: "active"                 │
└────────────┬────────────────────────┘
             │
             ├─► Staff sees alert on dashboard
             │
             ├─► Acknowledges alert (POST /alerts/{id}/acknowledge)
             │   Status: "acknowledged"
             │
             └─► Refills IV Bag
                 (IV level rises > 30%)
                 ├─► System auto-resolves alert
                 │   Status: "resolved"
                 │   Alert removed from active list
```

## 🧪 Testing with cURL

### 1. Send Sensor Data
```bash
curl -X POST http://localhost:8000/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device_001",
    "iv_level": 75.5,
    "drip_rate": 45.2,
    "temperature": 22.5
  }'
```

### 2. Get Dashboard Status
```bash
curl http://localhost:8000/dashboard?device_id=device_001
```

### 3. Get Prediction
```bash
curl http://localhost:8000/prediction?device_id=device_001
```

### 4. Get Active Alerts
```bash
curl http://localhost:8000/alerts
```

### 5. Generate Simulation Data (Testing)
```bash
curl -X POST http://localhost:8000/simulate/device_001
```

## 📈 Database Schema

### SensorData Table
Stores all IoT sensor readings.
```sql
CREATE TABLE sensor_data (
  id INTEGER PRIMARY KEY,
  device_id TEXT,
  iv_level FLOAT,
  drip_rate FLOAT,
  temperature FLOAT,
  timestamp DATETIME,
  created_at DATETIME
);
```

### Alert Table
Tracks all alert events.
```sql
CREATE TABLE alerts (
  id INTEGER PRIMARY KEY,
  device_id TEXT,
  alert_type TEXT,  -- 'critical', 'warning', 'info'
  iv_level FLOAT,
  message TEXT,
  status TEXT,  -- 'active', 'acknowledged', 'resolved'
  triggered_at DATETIME,
  acknowledged_at DATETIME,
  resolved_at DATETIME,
  buzzer_triggered BOOLEAN
);
```

### Prediction Table
Stores AI predictions.
```sql
CREATE TABLE predictions (
  id INTEGER PRIMARY KEY,
  device_id TEXT,
  estimated_finish_time DATETIME,
  confidence_score FLOAT,
  calculated_at DATETIME,
  iv_level_at_calc FLOAT,
  drip_rate_at_calc FLOAT
);
```

### DeviceStatus Table
Current status for quick dashboard queries.
```sql
CREATE TABLE device_status (
  id INTEGER PRIMARY KEY,
  device_id TEXT UNIQUE,
  current_iv_level FLOAT,
  current_drip_rate FLOAT,
  status_color TEXT,
  last_reading_at DATETIME,
  is_active BOOLEAN,
  updated_at DATETIME
);
```

## ⚙️ Configuration

Edit `config.py` to customize thresholds and settings:

```python
# Alert thresholds
ALERT_CRITICAL_LEVEL = 30     # Red alert at < 30%
ALERT_WARNING_LEVEL = 60      # Yellow alert at 30-60%

# IV monitoring
MAX_IV_VOLUME = 500           # Maximum IV capacity (mL)
DRIP_RATE_MIN = 10            # Minimum drip rate (mL/min)
DRIP_RATE_MAX = 200           # Maximum drip rate (mL/min)

# Prediction
MIN_HISTORY_POINTS = 3        # Min data points for prediction
```

## 🐳 Docker Deployment

Build and run with Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
```

Build:
```bash
docker build -t iv-monitoring-backend .
```

Run:
```bash
docker run -p 8000:8000 iv-monitoring-backend
```

## 📦 Database Migration to PostgreSQL

For production, switch to PostgreSQL:

```python
# In config.py
DATABASE_URL = "postgresql://user:password@localhost/iv_monitoring"
```

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

## 🔒 Security Notes

- **Production**: Change CORS `allow_origins` from `["*"]`
- **Authentication**: Add JWT/API key validation before deployment
- **Database**: Use environment variables for connection strings
- **HTTPS**: Deploy behind reverse proxy (Nginx, Cloud Load Balancer)
- **Rate Limiting**: Consider adding rate limiter for production
- **Input Validation**: All sensor values are validated

## 🐛 Logging & Debugging

Enable debug logging:
```python
# In config.py
DEBUG = True
```

View logs:
```bash
python app.py
```

Logs include:
- Sensor data ingestion
- Alert triggers and notifications
- Prediction calculations
- WebSocket connections
- Performance timestamps

## 🤝 Integration Example (Frontend)

### React Dashboard Component
```javascript
import React, { useEffect, useState } from 'react';

function Dashboard({ deviceId }) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    // Connect WebSocket for real-time updates
    const ws = new WebSocket(`ws://localhost:8000/ws/${deviceId}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(data);
    };

    // Initial dashboard fetch
    fetch(`http://localhost:8000/dashboard?device_id=${deviceId}`)
      .then(r => r.json())
      .then(data => setStatus(data[0]));

    return () => ws.close();
  }, [deviceId]);

  if (!status) return <div>Loading...</div>;

  return (
    <div>
      <h1>IV Monitor: {status.device_id}</h1>
      <p>IV Level: {status.current_iv_level}%</p>
      <p>Drip Rate: {status.current_drip_rate} mL/min</p>
      <div style={{
        backgroundColor: status.status_color,
        width: '100px',
        height: '100px'
      }}></div>
    </div>
  );
}

export default Dashboard;
```

## 📞 Support & Troubleshooting

**Port already in use:**
```bash
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

**Database locked:**
- Delete `iv_monitoring.db` and restart
- SQLite supports only one writer at a time

**WebSocket connection fails:**
- Ensure firewall allows WebSocket connections
- Check CORS configuration

## 📄 License

MIT License - Use freely for educational and commercial projects.

## 🎉 Next Steps

1. ✅ Run backend with `python app.py`
2. ✅ Test endpoints at http://localhost:8000/docs
3. ✅ Send sample sensor data via `/simulate/{device_id}`
4. ✅ Build frontend dashboard with WebSocket integration
5. ✅ Deploy to production with PostgreSQL & HTTPS
