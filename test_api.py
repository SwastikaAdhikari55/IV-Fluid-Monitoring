"""
Testing Script for IV Monitoring System

This script demonstrates how to interact with the API:
- Send sensor data
- Query dashboard
- Get predictions
- Manage alerts
- Test WebSocket connections

Run this after starting the backend: python app.py
Then run: python test_api.py
"""

import requests
import json
import time
import asyncio
import websockets
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_DEVICE_ID = "device_001"


def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health_check():
    """Test 1: Health check"""
    print_section("TEST 1: Health Check")

    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200


def test_send_sensor_data():
    """Test 2: Send sensor data"""
    print_section("TEST 2: Send Sensor Data (Green Status)")

    payload = {
        "device_id": TEST_DEVICE_ID,
        "iv_level": 85.5,
        "drip_rate": 45.2,
        "temperature": 22.5
    }

    print(f"Sending: {json.dumps(payload, indent=2)}")

    response = requests.post(f"{BASE_URL}/sensor-data", json=payload)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200


def test_send_warning_data():
    """Test 3: Send data that triggers warning (Yellow)"""
    print_section("TEST 3: Send Sensor Data (Yellow Status)")

    payload = {
        "device_id": TEST_DEVICE_ID,
        "iv_level": 45.0,
        "drip_rate": 30.0,
        "temperature": 22.5
    }

    print(f"Sending: {json.dumps(payload, indent=2)}")

    response = requests.post(f"{BASE_URL}/sensor-data", json=payload)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200


def test_send_critical_data():
    """Test 4: Send data that triggers critical alert (Red)"""
    print_section("TEST 4: Send Sensor Data (Red Status - Triggers Alert)")

    payload = {
        "device_id": TEST_DEVICE_ID,
        "iv_level": 20.0,
        "drip_rate": 25.0,
        "temperature": 22.5
    }

    print(f"Sending: {json.dumps(payload, indent=2)}")
    print("⚠️  This should trigger a CRITICAL alert!")

    response = requests.post(f"{BASE_URL}/sensor-data", json=payload)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200


def test_get_dashboard():
    """Test 5: Get dashboard status"""
    print_section("TEST 5: Get Dashboard Status")

    response = requests.get(f"{BASE_URL}/dashboard?device_id={TEST_DEVICE_ID}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    if data:
        alert_count = data[0].get("active_alerts", 0)
        print(f"\n✓ Device: {data[0]['device_id']}")
        print(f"✓ IV Level: {data[0]['current_iv_level']}%")
        print(f"✓ Drip Rate: {data[0]['current_drip_rate']} mL/min")
        print(f"✓ Status: {data[0]['status_color'].upper()}")
        print(f"✓ Active Alerts: {alert_count}")

    return response.status_code == 200


def test_get_prediction():
    """Test 6: Get AI prediction"""
    print_section("TEST 6: Get AI Prediction for IV Finish Time")

    response = requests.get(f"{BASE_URL}/prediction?device_id={TEST_DEVICE_ID}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    if response.status_code == 200:
        print(f"\n📊 Prediction Results:")
        print(f"✓ Estimated Finish: {data['estimated_finish_time']}")
        print(f"✓ Minutes Remaining: {data['minutes_remaining']}")
        print(f"✓ Confidence: {data['confidence_score']*100:.1f}%")
        print(f"✓ Based on {data['based_on_readings']} readings")

    return response.status_code == 200


def test_get_alerts():
    """Test 7: Get active alerts"""
    print_section("TEST 7: Get Active Alerts")

    response = requests.get(f"{BASE_URL}/alerts?device_id={TEST_DEVICE_ID}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    if data:
        print(f"\n⚠️  {len(data)} active alert(s) found:")
        for alert in data:
            print(f"  - [{alert['alert_type'].upper()}] {alert['message']}")
            print(f"    Status: {alert['status']}")
    else:
        print("\n✓ No active alerts")

    return response.status_code == 200


def test_acknowledge_alert():
    """Test 8: Acknowledge alert"""
    print_section("TEST 8: Acknowledge Alert")

    # First get active alerts
    response = requests.get(f"{BASE_URL}/alerts?device_id={TEST_DEVICE_ID}")
    alerts = response.json()

    if not alerts:
        print("No active alerts to acknowledge")
        return True

    alert_id = alerts[0]['id']
    print(f"Acknowledging alert ID: {alert_id}")

    response = requests.post(f"{BASE_URL}/alerts/{alert_id}/acknowledge")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200


def test_simulate_sensor():
    """Test 9: Simulate sensor data"""
    print_section("TEST 9: Simulate Sensor Data (For Testing)")

    print("Generating 5 simulated readings...\n")

    for i in range(5):
        response = requests.post(f"{BASE_URL}/simulate/{TEST_DEVICE_ID}")
        data = response.json()

        print(f"Reading {i+1}: IV Level: {data['iv_level']:.1f}%, "
              f"Drip Rate: {data['drip_rate']:.1f} mL/min, "
              f"Status: {data['status_color'].upper()}")

        if response.status_code == 200:
            time.sleep(1)  # Wait between readings
        else:
            print(f"Error: {data}")
            return False

    print("\n✓ Simulation complete")
    return True


async def test_websocket():
    """Test 10: WebSocket real-time connection"""
    print_section("TEST 10: WebSocket Real-Time Connection")

    try:
        ws_url = f"ws://localhost:8000/ws/{TEST_DEVICE_ID}"
        print(f"Connecting to: {ws_url}\n")

        async with websockets.connect(ws_url) as websocket:
            print("✓ WebSocket connected!")
            print("Waiting for messages (generating sensor data in 2 seconds)...\n")

            # Start generating data in a task
            async def send_data():
                await asyncio.sleep(2)
                for i in range(3):
                    requests.post(f"{BASE_URL}/simulate/{TEST_DEVICE_ID}")
                    await asyncio.sleep(1)

            send_task = asyncio.create_task(send_data())

            # Receive messages for 10 seconds
            start_time = time.time()
            while time.time() - start_time < 10:
                try:
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=1
                    )
                    data = json.loads(message)
                    print(f"📨 Message received: {json.dumps(data, indent=2)}\n")
                except asyncio.TimeoutError:
                    continue

            await send_task

        print("✓ WebSocket test complete")
        return True

    except Exception as e:
        print(f"✗ WebSocket error: {e}")
        print("Make sure the backend is running: python app.py")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "IV MONITORING SYSTEM - API TEST SUITE" + " "*10 + "║")
    print("╚" + "="*58 + "╝")

    tests = [
        ("Health Check", test_health_check),
        ("Send Green Status Data", test_send_sensor_data),
        ("Send Yellow Status Data", test_send_warning_data),
        ("Send Red Status Data (Alert)", test_send_critical_data),
        ("Get Dashboard", test_get_dashboard),
        ("Get Prediction", test_get_prediction),
        ("Get Alerts", test_get_alerts),
        ("Acknowledge Alert", test_acknowledge_alert),
        ("Simulate Sensor Data", test_simulate_sensor),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error: {e}")
            results.append((name, False))

    # WebSocket test (async)
    try:
        result = asyncio.run(test_websocket())
        results.append(("WebSocket Connection", result))
    except Exception as e:
        print(f"\n✗ WebSocket Error: {e}")
        results.append(("WebSocket Connection", False))

    # Print summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'='*60}\n")

    return passed == total


if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running: python app.py\n")
    input("Press Enter to start tests...")

    success = run_all_tests()
    exit(0 if success else 1)
