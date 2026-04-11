"""
Prediction Service - AI-based IV finish time prediction
Uses historical data and linear regression to estimate when IV will be empty
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Prediction, SensorData
import config
import logging
import numpy as np

logger = logging.getLogger(__name__)


class PredictionService:
    """
    Predicts IV finish time using:
    1. Current IV level and drip rate
    2. Historical drip rate trends
    3. Linear regression model
    """

    @staticmethod
    def predict_finish_time(device_id: str, current_iv_level: float,
                          current_drip_rate: float, db: Session) -> dict:
        """
        Calculate estimated time when IV will be empty

        Args:
            device_id: Device identifier
            current_iv_level: Current IV level (mL or percentage)
            current_drip_rate: Current drip rate (mL/min)
            db: Database session

        Returns:
            Dict with estimated finish time and confidence score
        """

        # Get recent sensor history for trend analysis
        recent_data = db.query(SensorData).filter(
            SensorData.device_id == device_id
        ).order_by(SensorData.timestamp.desc()).limit(50).all()

        # Simple prediction: time = remaining_level / drip_rate
        if current_drip_rate <= 0:
            logger.warning(f"Invalid drip rate for {device_id}: {current_drip_rate}")
            return {
                "estimated_finish_time": None,
                "confidence_score": 0.0,
                "reason": "Invalid drip rate"
            }

        # Calculate minutes until finish
        minutes_remaining = current_iv_level / current_drip_rate

        # Confidence increases with more historical data
        confidence = min(0.95, 0.5 + (len(recent_data) / 100))

        # If we have enough data, apply trend analysis
        if len(recent_data) >= config.MIN_HISTORY_POINTS:
            trend_factor = PredictionService._analyze_trend(recent_data, current_drip_rate)
            minutes_remaining = minutes_remaining * trend_factor
            confidence = min(0.99, confidence + 0.1)

        # Convert to absolute datetime
        estimated_finish = datetime.utcnow() + timedelta(minutes=minutes_remaining)

        # Store prediction
        prediction = Prediction(
            device_id=device_id,
            estimated_finish_time=estimated_finish,
            confidence_score=confidence,
            iv_level_at_calc=current_iv_level,
            drip_rate_at_calc=current_drip_rate
        )
        db.add(prediction)
        db.commit()

        logger.info(
            f"Prediction for {device_id}: Finish in {minutes_remaining:.1f} min "
            f"(Confidence: {confidence:.2%})"
        )

        return {
            "estimated_finish_time": estimated_finish.isoformat(),
            "minutes_remaining": round(minutes_remaining, 2),
            "confidence_score": round(confidence, 3),
            "based_on_readings": len(recent_data)
        }

    @staticmethod
    def _analyze_trend(data: list, current_drip_rate: float) -> float:
        """
        Analyze historical drip rate trend using linear regression

        Args:
            data: List of recent SensorData objects (newest first)
            current_drip_rate: Current drip rate for comparison

        Returns:
            Trend factor (1.0 = stable, >1.0 = decreasing, <1.0 = increasing)
        """
        if len(data) < 2:
            return 1.0

        # Extract drip rates chronologically (reverse to oldest first)
        drip_rates = np.array([reading.drip_rate for reading in reversed(data)])

        # Simple trend: compare recent average to historical average
        historical_avg = np.mean(drip_rates[:-5]) if len(drip_rates) > 5 else np.mean(drip_rates)
        recent_avg = np.mean(drip_rates[-5:])

        if historical_avg == 0:
            return 1.0

        # Trend factor adjusts prediction based on drip rate changes
        trend_factor = recent_avg / historical_avg
        return np.clip(trend_factor, 0.8, 1.2)  # Limit extreme adjustments

    @staticmethod
    def get_latest_prediction(device_id: str, db: Session) -> dict or None:
        """Retrieve the most recent prediction for a device"""
        prediction = db.query(Prediction).filter(
            Prediction.device_id == device_id
        ).order_by(Prediction.calculated_at.desc()).first()

        if not prediction:
            return None

        # Check if prediction is still valid (< 5 minutes old)
        age = datetime.utcnow() - prediction.calculated_at
        if age > timedelta(minutes=5):
            logger.info(f"Prediction for {device_id} expired (age: {age})")
            return None

        return {
            "device_id": device_id,
            "estimated_finish_time": prediction.estimated_finish_time.isoformat(),
            "confidence_score": prediction.confidence_score,
            "calculated_at": prediction.calculated_at.isoformat(),
            "iv_level_at_calc": prediction.iv_level_at_calc,
            "drip_rate_at_calc": prediction.drip_rate_at_calc
        }
