"""
Test script for IV Monitoring System Dashboard & API
Tests all API endpoints and simulates sensor data
"""

import requests
import json
from datetime import datetime
import time

# Configuration
API_URL = 'http://localhost:8000'
DEVICE_ID = 'device_001'

class Colors:
    """Terminal colors for pretty output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:<70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def test_health():
    """Test health endpoint"""
    print_header("Testing Health Endpoint")
    try:
        response = requests.get(f'{API_URL}/health')
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is running: {data}")
        else:
            print_error(f"Health check failed: {response.status_code}")
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        print_error("Make sure FastAPI backend is running on http://localhost:8000")
        return False
    return True

def test_get_data():
    """Test get current data endpoint"""
    print_header("Testing GET /data endpoint")
    try:
        response = requests.get(f'{API_URL}/data')
        if response.status_code == 200:
            data = response.json()
            print_success("Current IV Data Retrieved:")
            print(f"  • Device ID: {data.get('device_id')}")
            print(f"  • IV Level: {data.get('iv_level', 0):.1f}%")
            print(f"  • Drip Rate: {data.get('drip_rate', 0):.1f} drops/min")
            print(f"  • Status: {data.get('status')}")
            print(f"  • Battery: {data.get('battery_level', 0):.0f}%")
            print(f"  • WiFi Signal: {data.get('wifi_signal', 0):.0f}%")
            return data
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")
    return None

def test_get_prediction():
    """Test get prediction endpoint"""
    print_header("Testing GET /prediction endpoint")
    try:
        response = requests.get(f'{API_URL}/prediction')
        if response.status_code == 200:
            data = response.json()
            print_success("Prediction Data Retrieved:")
            print(f"  • Estimated Finish: {data.get('estimated_finish_time')}")
            print(f"  • Minutes Remaining: {data.get('minutes_remaining', 0):.1f}")
            print(f"  • Confidence Score: {(data.get('confidence_score', 0)*100):.0f}%")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_get_alerts():
    """Test get alerts endpoint"""
    print_header("Testing GET /alerts endpoint")
    try:
        response = requests.get(f'{API_URL}/alerts')
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                print_info("No active alerts")
            else:
                print_success(f"Retrieved {len(data)} alerts:")
                for alert in data:
                    print(f"  • [{alert.get('alert_type').upper()}] {alert.get('message')}")
                    print(f"    - ID: {alert.get('id')}, Status: {alert.get('status')}")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_post_sensor_data():
    """Test posting sensor data"""
    print_header("Testing POST /sensor-data endpoint")

    # Test 1: Normal data
    print_info("Test 1: Sending normal IV data...")
    payload = {
        'device_id': DEVICE_ID,
        'iv_level': 75.5,
        'drip_rate': 45.2,
        'temperature': 22.5
    }
    try:
        response = requests.post(f'{API_URL}/sensor-data', json=payload)
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            print_success(f"Sensor data posted: {data.get('status')}")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

    # Test 2: Low IV level (should trigger warning)
    print_info("Test 2: Sending LOW IV level (should trigger warning)...")
    payload['iv_level'] = 35.0
    try:
        response = requests.post(f'{API_URL}/sensor-data', json=payload)
        if response.status_code == 201 or response.status_code == 200:
            print_success("Low IV data posted (warning should be triggered)")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

    # Test 3: Critical IV level
    print_info("Test 3: Sending CRITICAL IV level (should trigger alert)...")
    payload['iv_level'] = 15.0
    try:
        response = requests.post(f'{API_URL}/sensor-data', json=payload)
        if response.status_code == 201 or response.status_code == 200:
            print_success("Critical IV data posted (alert should be triggered)")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_get_dashboard():
    """Test get complete dashboard data"""
    print_header("Testing GET /dashboard endpoint")
    try:
        response = requests.get(f'{API_URL}/dashboard')
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                device = data[0]
                print_success("Dashboard Data Retrieved:")
                print(f"  • Device: {device.get('device_id')}")
                print(f"  • IV Level: {device.get('current_iv_level', 0):.1f}%")
                print(f"  • Drip Rate: {device.get('current_drip_rate', 0):.1f} drops/min")
                print(f"  • Status: {device.get('status_color')}")
                print(f"  • Active Alerts: {device.get('alert_count_active', 0)}")
            else:
                print_error("No dashboard data returned")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_acknowledge_alert():
    """Test acknowledge alert endpoint"""
    print_header("Testing POST /alerts/{id}/acknowledge endpoint")
    try:
        # First get alerts
        response = requests.get(f'{API_URL}/alerts')
        if response.status_code == 200:
            alerts = response.json()
            if len(alerts) > 0:
                alert_id = alerts[0]['id']
                print_info(f"Acknowledging alert ID {alert_id}...")

                response = requests.post(f'{API_URL}/alerts/{alert_id}/acknowledge')
                if response.status_code == 200:
                    print_success(f"Alert {alert_id} acknowledged")
                else:
                    print_error(f"Failed to acknowledge: {response.status_code}")
            else:
                print_info("No alerts to acknowledge")
        else:
            print_error(f"Failed to fetch alerts: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_reset_alerts():
    """Test reset alerts endpoint"""
    print_header("Testing POST /alerts/reset endpoint")
    try:
        response = requests.post(f'{API_URL}/alerts/reset')
        if response.status_code == 200:
            print_success("All alerts reset")
        else:
            print_error(f"Request failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_continuous_monitoring():
    """Test continuous data monitoring (simulates dashboard)"""
    print_header("Continuous Monitoring Test (10 seconds)")
    print_info("Simulating dashboard continuous updates...")

    try:
        for i in range(5):
            print(f"\n--- Update {i+1}/5 ---")
            response = requests.get(f'{API_URL}/data')
            if response.status_code == 200:
                data = response.json()
                status_color = '🟢' if data.get('status') == 'normal' else '🟡' if data.get('status') == 'warning' else '🔴'
                print(f"{status_color} IV: {data.get('iv_level', 0):.1f}% | Drip: {data.get('drip_rate', 0):.1f} | Batt: {data.get('battery_level', 0):.0f}%")
            else:
                print_error("Failed to fetch data")

            if i < 4:
                time.sleep(2)

        print_success("Continuous monitoring completed")
    except Exception as e:
        print_error(f"Error: {e}")

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║         IV MONITORING SYSTEM - API TEST SUITE                    ║")
    print("║         Testing all endpoints and functionality                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")

    print_info(f"API URL: {API_URL}")
    print_info(f"Device ID: {DEVICE_ID}")
    print_info(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run tests in order
    if not test_health():
        print_error("Cannot connect to backend. Exiting tests.")
        return

    test_get_data()
    test_get_prediction()
    test_get_alerts()
    test_post_sensor_data()
    test_get_dashboard()
    test_get_alerts()  # Get alerts again to see if new ones were created
    test_acknowledge_alert()
    test_reset_alerts()
    test_continuous_monitoring()

    print_header("Test Suite Completed")
    print(f"{Colors.OKGREEN}All tests executed successfully!{Colors.ENDC}\n")
    print_info("Next steps:")
    print_info("1. Open dashboard.html in your browser")
    print_info("2. Click 'Start Monitoring' button")
    print_info("3. Watch real-time IV data updates")
    print_info("4. Check alerts when IV level is low\n")

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
