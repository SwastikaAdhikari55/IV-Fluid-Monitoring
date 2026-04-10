"""
FRONTEND INTEGRATION EXAMPLES
This file shows how to integrate the IV Monitoring System API with frontend applications.

Examples provided for:
1. Vanilla JavaScript (Browser)
2. React (Modern Frontend Framework)
3. Vue.js (Alternative Framework)
4. Python (Backend Integration)
"""

# ============================================================================
# 1. VANILLA JAVASCRIPT / HTML
# ============================================================================

"""
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>IV Monitoring Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .device-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-indicator {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
        .status-green { background-color: #4CAF50; }
        .status-yellow { background-color: #FFC107; }
        .status-red { background-color: #F44336; }
        .metric { margin: 10px 0; }
        .metric-label { font-weight: bold; }
        .alert { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; }
        .alert.critical { background-color: #f8d7da; border-left-color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>IV Monitoring System</h1>
        <div id="dashboard" class="dashboard"></div>
        <div id="alerts"></div>
    </div>

    <script>
        const API_URL = 'http://localhost:8000';
        const DEVICE_ID = 'device_001';

        class IVMonitoringDashboard {
            constructor() {
                this.ws = null;
                this.init();
            }

            async init() {
                // Connect WebSocket for real-time updates
                this.connectWebSocket();

                // Initial dashboard load
                await this.updateDashboard();

                // Poll every 5 seconds
                setInterval(() => this.updateDashboard(), 5000);
            }

            connectWebSocket() {
                this.ws = new WebSocket(`ws://localhost:8000/ws/${DEVICE_ID}`);

                this.ws.onopen = () => {
                    console.log('✓ WebSocket connected');
                };

                this.ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    console.log('Real-time update:', data);

                    if (data.type === 'sensor_update') {
                        this.updateDashboardUI(data);
                    }
                };

                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };

                this.ws.onclose = () => {
                    console.log('WebSocket disconnected, retrying...');
                    setTimeout(() => this.connectWebSocket(), 3000);
                };
            }

            async updateDashboard() {
                try {
                    // Fetch current status
                    const response = await fetch(
                        `${API_URL}/dashboard?device_id=${DEVICE_ID}`
                    );
                    const devices = await response.json();

                    if (devices.length === 0) return;

                    const device = devices[0];
                    this.updateDashboardUI(device);

                    // Fetch alerts
                    await this.updateAlerts();
                } catch (error) {
                    console.error('Error updating dashboard:', error);
                }
            }

            updateDashboardUI(device) {
                const html = `
                    <div class="device-card">
                        <div>
                            <h2>${device.device_id}
                                <span class="status-indicator status-${device.status_color}"></span>
                            </h2>
                        </div>
                        <div class="metric">
                            <span class="metric-label">IV Level:</span>
                            ${device.current_iv_level.toFixed(1)}%
                        </div>
                        <div class="metric">
                            <span class="metric-label">Drip Rate:</span>
                            ${device.current_drip_rate.toFixed(1)} mL/min
                        </div>
                        <div class="metric">
                            <span class="metric-label">Status:</span>
                            ${device.status_color.toUpperCase()}
                        </div>
                        ${device.prediction ? `
                            <div class="metric">
                                <span class="metric-label">Finish Time:</span>
                                ${this.formatTime(device.prediction.estimated_finish_time)}
                            </div>
                            <div class="metric">
                                <span class="metric-label">Confidence:</span>
                                ${(device.prediction.confidence_score * 100).toFixed(0)}%
                            </div>
                        ` : ''}
                    </div>
                `;

                document.getElementById('dashboard').innerHTML = html;
            }

            async updateAlerts() {
                try {
                    const response = await fetch(
                        `${API_URL}/alerts?device_id=${DEVICE_ID}`
                    );
                    const alerts = await response.json();

                    let html = '<h3>Active Alerts</h3>';
                    if (alerts.length === 0) {
                        html += '<p style="color: green;">✓ No active alerts</p>';
                    } else {
                        alerts.forEach(alert => {
                            const alertClass = alert.alert_type === 'critical' ? 'critical' : '';
                            html += `
                                <div class="alert ${alertClass}">
                                    <strong>[${alert.alert_type.toUpperCase()}]</strong>
                                    ${alert.message}
                                    <br>
                                    <small>Status: ${alert.status}</small>
                                    ${alert.alert_type === 'critical' ? `
                                        <button onclick="acknowledgeAlert(${alert.id})">
                                            Acknowledge
                                        </button>
                                    ` : ''}
                                </div>
                            `;
                        });
                    }

                    document.getElementById('alerts').innerHTML = html;
                } catch (error) {
                    console.error('Error fetching alerts:', error);
                }
            }

            formatTime(iso) {
                return new Date(iso).toLocaleTimeString();
            }
        }

        // Initialize dashboard
        new IVMonitoringDashboard();

        // Acknowledge alert
        async function acknowledgeAlert(alertId) {
            await fetch(`${API_URL}/alerts/${alertId}/acknowledge`, {
                method: 'POST'
            });
            location.reload();
        }

        // Send test sensor data
        async function sendTestData() {
            await fetch(`${API_URL}/sensor-data`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    device_id: DEVICE_ID,
                    iv_level: Math.random() * 100,
                    drip_rate: 20 + Math.random() * 50,
                    temperature: 22.5
                })
            });
        }
    </script>
</body>
</html>
"""


# ============================================================================
# 2. REACT COMPONENT EXAMPLE
# ============================================================================

"""
import React, { useEffect, useState, useCallback } from 'react';

const IVDashboard = ({ deviceId = 'device_001' }) => {
  const [device, setDevice] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:8000';

  // Fetch dashboard data
  const fetchDashboard = useCallback(async () => {
    try {
      const response = await fetch(
        `${API_URL}/dashboard?device_id=${deviceId}`
      );
      const data = await response.json();
      if (data.length > 0) {
        setDevice(data[0]);
      }
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }, [deviceId]);

  // Fetch alerts
  const fetchAlerts = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/alerts?device_id=${deviceId}`);
      const data = await response.json();
      setAlerts(data);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    }
  }, [deviceId]);

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${deviceId}`);

    ws.onopen = () => console.log('WebSocket connected');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'sensor_update') {
        setDevice(prev => ({
          ...prev,
          current_iv_level: data.iv_level,
          current_drip_rate: data.drip_rate,
          status_color: data.status_color
        }));
      }
    };

    return () => ws.close();
  }, [deviceId]);

  // Initial load and polling
  useEffect(() => {
    fetchDashboard();
    fetchAlerts();
    setLoading(false);

    const dashboardInterval = setInterval(fetchDashboard, 5000);
    const alertsInterval = setInterval(fetchAlerts, 3000);

    return () => {
      clearInterval(dashboardInterval);
      clearInterval(alertsInterval);
    };
  }, [fetchDashboard, fetchAlerts]);

  const getStatusColor = (color) => {
    const colors = { green: '#4CAF50', yellow: '#FFC107', red: '#F44336' };
    return colors[color] || '#ccc';
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!device) return <div>No device data</div>;

  return (
    <div style={{ fontFamily: 'Arial', padding: '20px', maxWidth: '800px' }}>
      <h1>IV Monitoring Dashboard</h1>

      <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
        <h2>{device.device_id}</h2>

        <div style={{
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: getStatusColor(device.status_color),
          display: 'inline-block',
          marginBottom: '20px'
        }}></div>

        <div><strong>IV Level:</strong> {device.current_iv_level.toFixed(1)}%</div>
        <div><strong>Drip Rate:</strong> {device.current_drip_rate.toFixed(1)} mL/min</div>
        <div><strong>Status:</strong> {device.status_color.toUpperCase()}</div>

        {device.prediction && (
          <div style={{ marginTop: '20px', borderTop: '1px solid #ddd', paddingTop: '20px' }}>
            <h3>Prediction</h3>
            <div><strong>Finish Time:</strong> {new Date(device.prediction.estimated_finish_time).toLocaleTimeString()}</div>
            <div><strong>Minutes Remaining:</strong> {device.prediction.minutes_remaining.toFixed(1)}</div>
            <div><strong>Confidence:</strong> {(device.prediction.confidence_score * 100).toFixed(0)}%</div>
          </div>
        )}
      </div>

      {alerts.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3>Active Alerts ({alerts.length})</h3>
          {alerts.map((alert) => (
            <div
              key={alert.id}
              style={{
                backgroundColor: alert.alert_type === 'critical' ? '#f8d7da' : '#fff3cd',
                borderLeft: `4px solid ${alert.alert_type === 'critical' ? '#f44336' : '#ffc107'}`,
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '4px'
              }}
            >
              <strong>[{alert.alert_type.toUpperCase()}]</strong>
              <p>{alert.message}</p>
              <small>Status: {alert.status}</small>
              {alert.alert_type === 'critical' && (
                <button
                  onClick={async () => {
                    await fetch(`http://localhost:8000/alerts/${alert.id}/acknowledge`, {
                      method: 'POST'
                    });
                    fetchAlerts();
                  }}
                  style={{
                    marginTop: '10px',
                    padding: '8px 16px',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Acknowledge
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default IVDashboard;
"""


# ============================================================================
# 3. PYTHON BACKEND INTEGRATION
# ============================================================================

"""
import requests
import asyncio
import websockets
import json
from datetime import datetime

class IVMonitoringClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.session = requests.Session()

    def send_sensor_data(self, device_id, iv_level, drip_rate, temperature=None):
        '''Send IoT sensor data to backend'''
        payload = {
            'device_id': device_id,
            'iv_level': iv_level,
            'drip_rate': drip_rate,
            'temperature': temperature
        }
        response = self.session.post(
            f'{self.base_url}/sensor-data',
            json=payload
        )
        return response.json()

    def get_dashboard(self, device_id=None):
        '''Get dashboard status'''
        params = {'device_id': device_id} if device_id else {}
        response = self.session.get(f'{self.base_url}/dashboard', params=params)
        return response.json()

    def get_prediction(self, device_id):
        '''Get IV finish time prediction'''
        response = self.session.get(
            f'{self.base_url}/prediction',
            params={'device_id': device_id}
        )
        return response.json()

    def get_alerts(self, device_id=None):
        '''Get active alerts'''
        params = {'device_id': device_id} if device_id else {}
        response = self.session.get(f'{self.base_url}/alerts', params=params)
        return response.json()

    async def connect_websocket(self, device_id, callback):
        '''Connect to WebSocket for real-time updates'''
        uri = f'ws://localhost:8000/ws/{device_id}'
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                await callback(data)

# Usage example
client = IVMonitoringClient()

# Send sensor data
result = client.send_sensor_data('device_001', 75.5, 45.2, 22.5)
print('Sensor data sent:', result)

# Get dashboard
dashboard = client.get_dashboard('device_001')
print('Dashboard:', dashboard)

# Get prediction
prediction = client.get_prediction('device_001')
print('Prediction:', prediction)

# Get alerts
alerts = client.get_alerts('device_001')
print('Alerts:', alerts)

# Real-time WebSocket
async def handle_update(data):
    print(f'Update: {data}')

asyncio.run(client.connect_websocket('device_001', handle_update))
"""
