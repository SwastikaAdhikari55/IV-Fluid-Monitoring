"""
Database models for IV Monitoring System
Defines the structure for sensor data, alerts, and predictions
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for all models
Base = declarative_base()


class SensorData(Base):
    """
    Stores IoT sensor readings for IV monitoring
    Tracks IV level (0-100%) and drip rate over time
    """
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)  # IoT device identifier
    iv_level = Column(Float)  # IV fluid level in mL or percentage
    drip_rate = Column(Float)  # mL/min
    temperature = Column(Float, nullable=True)  # Optional sensor temperature
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """
    Stores alert events triggered by IV monitoring thresholds
    Tracks alert status: pending, acknowledged, resolved
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    alert_type = Column(String)  # 'critical', 'warning', 'info'
    iv_level = Column(Float)  # IV level when alert triggered
    message = Column(String)
    status = Column(String, default="active")  # 'active', 'acknowledged', 'resolved'
    triggered_at = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    buzzer_triggered = Column(Boolean, default=False)


class Prediction(Base):
    """
    Stores AI predictions for IV finish time
    Calculated based on current level, drip rate, and historical data
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    estimated_finish_time = Column(DateTime)  # Predicted time when IV will be empty
    confidence_score = Column(Float)  # Prediction accuracy (0-1)
    calculated_at = Column(DateTime, default=datetime.utcnow, index=True)
    iv_level_at_calc = Column(Float)  # IV level when prediction was made
    drip_rate_at_calc = Column(Float)  # Drip rate when prediction was made


class DeviceStatus(Base):
    """
    Maintains current status for each IV monitoring device
    Provides quick lookup for dashboard without complex queries
    """
    __tablename__ = "device_status"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    current_iv_level = Column(Float)
    current_drip_rate = Column(Float)
    status_color = Column(String)  # 'green', 'yellow', 'red'
    last_reading_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Database initialization function
def init_db(database_url: str):
    """Initialize database engine and create all tables"""
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


def get_session_factory(engine):
    """Create session factory for database operations"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
