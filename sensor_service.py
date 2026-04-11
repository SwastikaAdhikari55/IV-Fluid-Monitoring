"""
Sensor Service - Handles IoT data ingestion and processing
Receives, validates, and processes sensor readings
"""

from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from models import SensorData, DeviceStatus, Alert
import config
import logging

logger = logging.getLogger(__name__)


class SensorService:
    """
    Manages sensor data lifecycle:
    - Receives data from IoT devices
    - Validates readings
    - Updates device status
    - Triggers processing pipeline
    """

    @staticmethod
    def ingest_sensor_data(device_id: str, iv_level: float, drip_rate: float,
                          temperature: Optional[float] = None, db = None) -> dict:  # type: ignore
        """
        Ingest and process IoT sensor reading

        Args:
            device_id: Identifier for the IV monitoring device
            iv_level: IV fluid level (0-100%)
            drip_rate: Drip rate in mL/min
            temperature: Optional sensor temperature reading
            db: Database session

        Returns:
            Dict with processing results and status
        """

        # Validate input ranges
        if not SensorService._validate_reading(iv_level, drip_rate):
            logger.error(f"Invalid sensor reading from {device_id}: level={iv_level}, rate={drip_rate}")
            return {"success": False, "error": "Invalid sensor values"}

        # Store sensor reading
        sensor_data = SensorData(
            device_id=device_id,
            iv_level=iv_level,
            drip_rate=drip_rate,
            temperature=temperature
        )
        db.add(sensor_data)  # type: ignore

        # Determine status color based on IV level
        status_color = SensorService._determine_status_color(iv_level)

        # Update or create device status
        device_status = db.query(DeviceStatus).filter(  # type: ignore
            DeviceStatus.device_id == device_id
        ).first()

        if device_status:
            device_status.current_iv_level = iv_level  # type: ignore
            device_status.current_drip_rate = drip_rate  # type: ignore
            device_status.status_color = status_color  # type: ignore
            device_status.last_reading_at = datetime.utcnow()  # type: ignore
        else:
            device_status = DeviceStatus(
                device_id=device_id,
                current_iv_level=iv_level,
                current_drip_rate=drip_rate,
                status_color=status_color,
                is_active=True
            )
            db.add(device_status)  # type: ignore

        db.commit()  # type: ignore

        logger.info(
            f"Sensor data ingested for {device_id}: "
            f"Level={iv_level:.1f}%, Rate={drip_rate:.1f}mL/min, Status={status_color}"
        )

        return {
            "success": True,
            "device_id": device_id,
            "iv_level": iv_level,
            "drip_rate": drip_rate,
            "status_color": status_color,
            "timestamp": sensor_data.timestamp.isoformat(),
            "message": f"Reading stored successfully. Status: {status_color.upper()}"
        }

    @staticmethod
    def _validate_reading(iv_level: float, drip_rate: float) -> bool:
        """
        Validate sensor readings against acceptable ranges

        Args:
            iv_level: IV level reading
            drip_rate: Drip rate reading

        Returns:
            True if valid, False otherwise
        """
        # IV level should be between 0-100% (or 0-500mL)
        if not (0 <= iv_level <= config.MAX_IV_VOLUME):
            return False

        # Drip rate should be within operational range (or zero for stopped)
        if drip_rate < 0 or drip_rate > config.DRIP_RATE_MAX:
            return False

        return True

    @staticmethod
    def _determine_status_color(iv_level: float) -> str:
        """
        Determine status indicator color based on IV level

        Args:
            iv_level: Current IV level

        Returns:
            Color string: 'green', 'yellow', or 'red'
        """
        if iv_level > config.ALERT_WARNING_LEVEL:
            return "green"
        elif iv_level >= config.ALERT_CRITICAL_LEVEL:
            return "yellow"
        else:
            return "red"

    @staticmethod
    def simulate_sensor_data(device_id: str, db: Session) -> dict:
        """
        Generate simulated sensor data for testing
        Simulates realistic IV drainage patterns

        Args:
            device_id: Device to generate data for
            db: Database session

        Returns:
            Generated sensor reading
        """
        import random

        # Get last reading or create initial state
        last_reading = db.query(SensorData).filter(  # type: ignore
            SensorData.device_id == device_id
        ).order_by(SensorData.timestamp.desc()).first()

        if last_reading:
            # Gradually decrease IV level by drip rate, add some noise
            iv_level = max(0, last_reading.iv_level - random.uniform(0.5, 2.5))
            drip_rate = last_reading.drip_rate + random.uniform(-5, 5)
        else:
            # Initial state: 80-100% full
            iv_level = random.uniform(80, 100)
            drip_rate = random.uniform(config.DRIP_RATE_MIN, config.DRIP_RATE_MAX)

        # Ensure valid ranges
        iv_level = max(0, min(100, iv_level))
        drip_rate = max(config.DRIP_RATE_MIN, min(config.DRIP_RATE_MAX, drip_rate))

        # Add temperature noise
        temperature = 22 + random.uniform(-1, 1)

        return SensorService.ingest_sensor_data(
            device_id=device_id,
            iv_level=round(float(iv_level), 2),  # type: ignore
            drip_rate=round(float(drip_rate), 2),  # type: ignore
            temperature=round(float(temperature), 1),  # type: ignore
            db=db
        )

    @staticmethod
    def get_device_history(device_id: str, limit: int = 100, db = None) -> list:  # type: ignore
        """Retrieve historical sensor data for a device"""
        readings = db.query(SensorData).filter(  # type: ignore
            SensorData.device_id == device_id
        ).order_by(SensorData.timestamp.desc()).limit(limit).all()

        return [{
            "timestamp": r.timestamp.isoformat(),
            "iv_level": r.iv_level,
            "drip_rate": r.drip_rate,
            "temperature": r.temperature
        } for r in reversed(readings)]
