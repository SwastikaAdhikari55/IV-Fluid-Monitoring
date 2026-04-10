"""
Configuration settings for IV Monitoring System
Environment-based configuration for development and production
"""

import os
from datetime import timedelta

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./iv_monitoring.db")

# API Configuration
API_TITLE = "IV Monitoring System API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Real-time IV fluid monitoring with AI prediction"

# Server Configuration
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Alert Configuration
ALERT_CRITICAL_LEVEL = 30  # Red alert threshold
ALERT_WARNING_LEVEL = 60   # Yellow alert threshold
ALERT_CHECK_INTERVAL = 5   # seconds

# IV Monitoring Configuration
MAX_IV_VOLUME = 500  # mL
DRIP_RATE_MIN = 10   # mL/min
DRIP_RATE_MAX = 200  # mL/min

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL = 5  # seconds

# Prediction Configuration
MIN_HISTORY_POINTS = 3  # Minimum data points for accurate prediction
