"""
Alert Service - Handles alert detection and management
Monitors IV levels and triggers alerts based on thresholds
"""

from datetime import datetime
from sqlalchemy.orm import Session
from models import Alert, SensorData, DeviceStatus
import config
import logging

logger = logging.getLogger(__name__)


class AlertService:
    """
    Manages alert lifecycle: creation, acknowledgment, resolution
    Simulates mobile notifications and buzzer alerts
    """

    @staticmethod
    def check_alert_status(device_id: str, iv_level: float, db: Session) -> Alert or None:
        """
        Determines if an alert should be triggered based on IV level

        Args:
            device_id: Device identifier
            iv_level: Current IV fluid level
            db: Database session

        Returns:
            Alert object if triggered, None otherwise
        """
        # Critical alert (Red) - IV < 30%
        if iv_level < config.ALERT_CRITICAL_LEVEL:
            alert_type = "critical"
            message = f"CRITICAL: IV level critically low ({iv_level:.1f}%)"
        # Warning alert (Yellow) - IV 30-60%
        elif iv_level < config.ALERT_WARNING_LEVEL:
            alert_type = "warning"
            message = f"WARNING: IV level low ({iv_level:.1f}%)"
        else:
            # Check if there's an active alert to resolve
            active_alert = db.query(Alert).filter(
                Alert.device_id == device_id,
                Alert.status == "active"
            ).first()
            if active_alert:
                AlertService.resolve_alert(active_alert.id, db)
            return None

        # Check if there's already an active alert of this type
        existing_alert = db.query(Alert).filter(
            Alert.device_id == device_id,
            Alert.alert_type == alert_type,
            Alert.status == "active"
        ).first()

        if existing_alert:
            return existing_alert  # Don't create duplicate

        # Create new alert
        alert = Alert(
            device_id=device_id,
            alert_type=alert_type,
            iv_level=iv_level,
            message=message,
            status="active"
        )
        db.add(alert)
        db.commit()

        logger.warning(f"Alert triggered for {device_id}: {message}")

        # Simulate notifications
        AlertService.send_mobile_notification(device_id, message)
        AlertService.trigger_buzzer(alert_type)

        return alert

    @staticmethod
    def send_mobile_notification(device_id: str, message: str):
        """
        Simulates sending mobile notification
        In production: integrate with Firebase Cloud Messaging, APNs, etc.
        """
        logger.info(f"📱 MOBILE NOTIFICATION [Device: {device_id}]: {message}")
        # TODO: Integrate with real push notification service
        # firebase_admin.messaging.send(...)

    @staticmethod
    def trigger_buzzer(alert_type: str):
        """
        Simulates buzzer alert for critical conditions
        In production: communicate with IoT device or alert system
        """
        if alert_type == "critical":
            logger.critical(f"🚨 BUZZER TRIGGERED (CRITICAL): BEEP BEEP BEEP!")
        elif alert_type == "warning":
            logger.warning(f"⚠️  BUZZER TRIGGERED (WARNING): beep beep")
        # TODO: In production, trigger actual device buzzer via MQTT, HTTP, etc.

    @staticmethod
    def acknowledge_alert(alert_id: int, db: Session):
        """Mark alert as acknowledged by staff"""
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.status = "acknowledged"
            alert.acknowledged_at = datetime.utcnow()
            db.commit()
            logger.info(f"Alert {alert_id} acknowledged")

    @staticmethod
    def resolve_alert(alert_id: int, db: Session):
        """Mark alert as resolved (IV refilled or level restored)"""
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.status = "resolved"
            alert.resolved_at = datetime.utcnow()
            db.commit()
            logger.info(f"Alert {alert_id} resolved")

    @staticmethod
    def get_active_alerts(device_id: str = None, db: Session = None) -> list:
        """Retrieve all active alerts, optionally filtered by device"""
        query = db.query(Alert).filter(Alert.status == "active")
        if device_id:
            query = query.filter(Alert.device_id == device_id)
        return query.all()
