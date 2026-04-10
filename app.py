"""
IV Monitoring System - Backend
Main FastAPI application with REST API endpoints and WebSocket support

Features:
- Real-time IV level monitoring with color-coded status
- IoT sensor data ingestion and validation
- AI-powered IV finish time prediction
- Automated alert system with mobile notifications and buzzer simulation
- Dashboard API for frontend integration
- WebSocket support for real-time updates
"""

from fastapi import FastAPI, HTTPException, WebSocket, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
import asyncio
from datetime import datetime

# Import configuration and services
import config
from models import init_db, get_session_factory, DeviceStatus, Alert
from sensor_service import SensorService
from alert_service import AlertService
from prediction_service import PredictionService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
engine = init_db(config.DATABASE_URL)
SessionLocal = get_session_factory(engine)

# Global storage for active WebSocket connections (for broadcasting)
active_connections: dict = {}


# ============================================================================
# Pydantic Models (Request/Response validation)
# ============================================================================

class SensorDataRequest(BaseModel):
    """Schema for IoT sensor data POST request"""
    device_id: str
    iv_level: float  # 0-100% or mL
    drip_rate: float  # mL/min
    temperature: float = None


class SensorDataResponse(BaseModel):
    """Response schema for sensor data endpoint"""
    success: bool
    device_id: str
    iv_level: float
    drip_rate: float
    status_color: str
    timestamp: str
    message: str


class DashboardResponse(BaseModel):
    """Dashboard status response"""
    device_id: str
    current_iv_level: float
    current_drip_rate: float
    status_color: str  # 'green', 'yellow', 'red'
    last_reading_at: str
    active_alerts: int
    prediction: dict | None = None


class AlertResponse(BaseModel):
    """Alert data response"""
    id: int
    device_id: str
    alert_type: str  # 'critical', 'warning', 'info'
    iv_level: float
    message: str
    status: str
    triggered_at: str
    acknowledged_at: str = None


class PredictionResponse(BaseModel):
    """Prediction data response"""
    device_id: str
    estimated_finish_time: str
    minutes_remaining: float
    confidence_score: float
    based_on_readings: int


# ============================================================================
# Helper Functions
# ============================================================================

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def broadcast_to_connections(device_id: str, message: dict):
    """
    Broadcast update to all connected WebSocket clients for a device
    Enables real-time dashboard updates
    """
    if device_id in active_connections:
        disconnected_clients = []
        for client in active_connections[device_id]:
            try:
                await client.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send WebSocket message: {e}")
                disconnected_clients.append(client)

        # Remove disconnected clients
        for client in disconnected_clients:
            active_connections[device_id].remove(client)
        if not active_connections[device_id]:
            del active_connections[device_id]


async def startup_event():
    """Initialize background tasks on startup"""
    logger.info("🚀 IV Monitoring System starting up...")
    logger.info(f"Database: {config.DATABASE_URL}")
    logger.info(f"Debug Mode: {config.DEBUG}")


async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 IV Monitoring System shutting down...")


# ============================================================================
# FastAPI App Setup
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle (startup/shutdown)"""
    await startup_event()
    yield
    await shutdown_event()


app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "IV Monitoring System",
        "version": config.API_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/sensor-data", response_model=SensorDataResponse, tags=["Sensor"])
async def receive_sensor_data(data: SensorDataRequest, db: Session = Depends(get_db)):
    """
    Receive IoT sensor data from monitoring devices

    **Example Request:**
    ```json
    {
        "device_id": "device_001",
        "iv_level": 75.5,
        "drip_rate": 45.2,
        "temperature": 22.5
    }
    ```

    **Response:**
    - success: Whether data was processed
    - status_color: Current IV status (green/yellow/red)
    - timestamp: When reading was recorded
    """
    try:
        # Ingest sensor data
        result = SensorService.ingest_sensor_data(
            device_id=data.device_id,
            iv_level=data.iv_level,
            drip_rate=data.drip_rate,
            temperature=data.temperature,
            db=db
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Check for alerts after processing
        alert = AlertService.check_alert_status(
            data.device_id,
            data.iv_level,
            db
        )

        # Broadcast to WebSocket clients
        await broadcast_to_connections(data.device_id, {
            "type": "sensor_update",
            "device_id": data.device_id,
            "iv_level": data.iv_level,
            "drip_rate": data.drip_rate,
            "status_color": result["status_color"],
            "timestamp": result["timestamp"]
        })

        return SensorDataResponse(**result)

    except Exception as e:
        logger.error(f"Error processing sensor data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard", response_model=list[DashboardResponse], tags=["Dashboard"])
async def get_dashboard(device_id: str = Query(None), db: Session = Depends(get_db)):
    """
    Get current dashboard status for device(s)

    **Query Parameters:**
    - device_id (optional): Specific device ID to query

    **Returns:**
    - IV level and drip rate
    - Status color (green/yellow/red)
    - Count of active alerts
    - Latest prediction if available

    **Example Response:**
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
                "confidence_score": 0.85
            }
        }
    ]
    ```
    """
    try:
        query = db.query(DeviceStatus)
        if device_id:
            query = query.filter(DeviceStatus.device_id == device_id)

        devices = query.all()
        if not devices:
            raise HTTPException(status_code=404, detail="No devices found")

        response = []
        for device in devices:
            active_alerts = len(AlertService.get_active_alerts(device.device_id, db))

            prediction = PredictionService.get_latest_prediction(device.device_id, db)

            response.append(DashboardResponse(
                device_id=device.device_id,
                current_iv_level=device.current_iv_level,
                current_drip_rate=device.current_drip_rate,
                status_color=device.status_color,
                last_reading_at=device.last_reading_at.isoformat(),
                active_alerts=active_alerts,
                prediction=prediction
            ))

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prediction", response_model=PredictionResponse, tags=["Prediction"])
async def get_prediction(device_id: str, db: Session = Depends(get_db)):
    """
    Get AI prediction for IV finish time

    **Query Parameters:**
    - device_id: Device ID to predict for

    **Returns:**
    - Estimated finish time (ISO format)
    - Minutes remaining
    - Confidence score (0-1)
    - Number of readings used

    **Features:**
    - Uses current IV level and drip rate
    - Analyzes historical trends
    - Confidence increases with more data points
    """
    try:
        device = db.query(DeviceStatus).filter(
            DeviceStatus.device_id == device_id
        ).first()

        if not device:
            raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

        prediction = PredictionService.predict_finish_time(
            device_id=device_id,
            current_iv_level=device.current_iv_level,
            current_drip_rate=device.current_drip_rate,
            db=db
        )

        return PredictionResponse(device_id=device_id, **prediction)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts", tags=["Alerts"])
async def get_alerts(device_id: str = Query(None), db: Session = Depends(get_db)):
    """
    Get active and historical alerts

    **Query Parameters:**
    - device_id (optional): Filter by specific device

    **Returns:**
    - Alert ID, type (critical/warning/info)
    - Current status (active/acknowledged/resolved)
    - Timestamps and messages

    **Alert Types:**
    - CRITICAL (Red): IV level < 30%
    - WARNING (Yellow): IV level 30-60%
    - INFO: IV level > 60%
    """
    try:
        query = db.query(Alert).filter(Alert.status.in_(["active", "acknowledged"]))
        if device_id:
            query = query.filter(Alert.device_id == device_id)

        alerts = query.order_by(Alert.triggered_at.desc()).all()

        return [{
            "id": alert.id,
            "device_id": alert.device_id,
            "alert_type": alert.alert_type,
            "iv_level": alert.iv_level,
            "message": alert.message,
            "status": alert.status,
            "triggered_at": alert.triggered_at.isoformat(),
            "acknowledged_at": alert.acknowledged_at.isoformat() if alert.acknowledged_at else None
        } for alert in alerts]

    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/{alert_id}/acknowledge", tags=["Alerts"])
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge an alert (mark as seen by staff)"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    AlertService.acknowledge_alert(alert_id, db)
    return {"success": True, "message": "Alert acknowledged"}


@app.delete("/alerts/{alert_id}", tags=["Alerts"])
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Resolve/clear an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    AlertService.resolve_alert(alert_id, db)
    return {"success": True, "message": "Alert resolved"}


@app.post("/simulate/{device_id}", tags=["Simulation"])
async def simulate_sensor_reading(device_id: str, db: Session = Depends(get_db)):
    """
    Generate simulated sensor data for testing
    Useful for development and demonstrations
    """
    try:
        result = SensorService.simulate_sensor_data(device_id, db)

        # Trigger alert check
        AlertService.check_alert_status(device_id, result["iv_level"], db)

        # Broadcast update
        await broadcast_to_connections(device_id, {
            "type": "simulated_update",
            "device_id": device_id,
            "iv_level": result["iv_level"],
            "drip_rate": result["drip_rate"],
            "status_color": result["status_color"]
        })

        return result

    except Exception as e:
        logger.error(f"Error simulating sensor data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WebSocket for Real-Time Updates
# ============================================================================

@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    """
    WebSocket connection for real-time dashboard updates

    **Usage:**
    ```
    ws://localhost:8000/ws/device_001
    ```

    **Receives:**
    - sensor_update: New IV level/drip rate
    - alert_triggered: New alert
    - prediction_update: New prediction
    """
    await websocket.accept()

    # Register connection
    if device_id not in active_connections:
        active_connections[device_id] = []
    active_connections[device_id].append(websocket)

    logger.info(f"WebSocket connection opened for {device_id}")

    try:
        while True:
            # Keep connection open and handle incoming messages
            data = await websocket.receive_text()
            logger.debug(f"WebSocket message from {device_id}: {data}")

    except Exception as e:
        logger.warning(f"WebSocket error for {device_id}: {e}")
    finally:
        # Cleanup connection
        if device_id in active_connections:
            active_connections[device_id].remove(websocket)
            if not active_connections[device_id]:
                del active_connections[device_id]
        logger.info(f"WebSocket connection closed for {device_id}")


# ============================================================================
# Background Tasks (Optional Enhancement)
# ============================================================================

async def alert_check_background_task():
    """
    Periodically check all active devices for alert conditions
    Can be enhanced with APScheduler for more sophisticated scheduling
    """
    logger.info("Alert check background task started")
    db = SessionLocal()
    try:
        while True:
            await asyncio.sleep(config.ALERT_CHECK_INTERVAL)
            # Add background alert checking logic here if needed
    finally:
        db.close()


# ============================================================================
# Running the Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting IV Monitoring System on {config.HOST}:{config.PORT}")
    logger.info("Access API at http://localhost:8000/docs")

    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="info",
        reload=config.DEBUG
    )
