"""
Configuration settings for Wind Farm AI Operator Dashboard
"""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SRC_DIR = PROJECT_ROOT / "src"

# Data files
SCADA_RAW = DATA_DIR / "wind_scada_5turbines_1month_realistic.csv"
SCADA_CLEAN = DATA_DIR / "wind_scada_clean.parquet"
POWER_CURVE = DATA_DIR / "power_curve_empirical.csv"
UNDERPERF_EVENTS = DATA_DIR / "underperformance_events.csv"
FAULT_DIAGNOSIS = DATA_DIR / "fault_diagnosis_results.csv"
TROUBLESHOOTING = DATA_DIR / "troubleshooting_recommendations.csv"
HEALTH_SCORES = DATA_DIR / "turbine_health_scores.csv"
REPORT_MD = DATA_DIR / "wind_farm_intelligent_report.md"
REPORT_PDF = DATA_DIR / "wind_farm_intelligent_report.pdf"

# Turbine Configuration
RATED_POWER_KW = 2000
INTERVAL_MIN = 10
TURBINE_IDS = ["T01", "T02", "T03", "T04", "T05"]

# Thresholds
THRESHOLDS = {
    "gear_oil_temp_limit": 85,  # °C
    "nacelle_temp_limit": 70,   # °C
    "vibration_high": 1.5,      # g-RMS
    "yaw_misalignment": 15,     # degrees
    "pitch_stuck_angle": 0.5,   # degrees
    "underperf_threshold": 0.2, # 20% below expected
}

# Health Score Weights
HEALTH_WEIGHTS = {
    "oil_temp_high": -30,
    "oil_slope_high": -20,
    "vibration_high": -30,
    "vib_slope_high": -20,
    "yaw_misalignment": -10,
}

# Severity Colors
SEVERITY_COLORS = {
    "CRITICAL": "#dc3545",
    "HIGH": "#fd7e14",
    "MEDIUM": "#ffc107",
    "LOW": "#28a745",
    "NONE": "#6c757d",
}

# Status Colors
STATUS_COLORS = {
    "green": "#28a745",
    "yellow": "#ffc107",
    "red": "#dc3545",
    "blue": "#007bff",
}

# Chart Theme
CHART_THEME = {
    "primary_color": "#1a5f7a",
    "secondary_color": "#2c7da0",
    "accent_color": "#61a5c2",
    "background_color": "#f8f9fa",
    "text_color": "#333333",
}

