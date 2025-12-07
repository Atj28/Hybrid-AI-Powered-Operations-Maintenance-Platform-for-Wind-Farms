"""
Data loading utilities for Wind Farm Dashboard
"""

import pandas as pd
import streamlit as st
from pathlib import Path
import sys

# Add config to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.settings import *


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_scada_data():
    """Load cleaned SCADA data"""
    try:
        df = pd.read_parquet(SCADA_CLEAN)
        return df
    except FileNotFoundError:
        st.error(f"SCADA data not found at {SCADA_CLEAN}")
        return None


@st.cache_data(ttl=300)
def load_fault_diagnosis():
    """Load fault diagnosis results"""
    try:
        df = pd.read_csv(FAULT_DIAGNOSIS, parse_dates=["timestamp"])
        return df
    except FileNotFoundError:
        st.warning("Fault diagnosis data not found. Run the pipeline first.")
        return None


@st.cache_data(ttl=300)
def load_troubleshooting():
    """Load troubleshooting recommendations"""
    try:
        df = pd.read_csv(TROUBLESHOOTING, parse_dates=["timestamp"])
        return df
    except FileNotFoundError:
        st.warning("Troubleshooting data not found. Run the pipeline first.")
        return None


@st.cache_data(ttl=300)
def load_health_scores():
    """Load turbine health scores"""
    try:
        df = pd.read_csv(HEALTH_SCORES)
        return df
    except FileNotFoundError:
        st.warning("Health scores not found. Run the pipeline first.")
        return None


@st.cache_data(ttl=300)
def load_underperformance():
    """Load underperformance events"""
    try:
        df = pd.read_csv(UNDERPERF_EVENTS, parse_dates=["timestamp"])
        return df
    except FileNotFoundError:
        st.warning("Underperformance data not found. Run the pipeline first.")
        return None


@st.cache_data(ttl=300)
def load_power_curve():
    """Load empirical power curve"""
    try:
        df = pd.read_csv(POWER_CURVE)
        return df
    except FileNotFoundError:
        st.warning("Power curve data not found. Run the pipeline first.")
        return None


def compute_farm_kpis(df: pd.DataFrame) -> dict:
    """Compute farm-level KPIs from SCADA data"""
    if df is None:
        return {}
    
    df = df.copy()
    df["energy_kwh"] = df["power_kw"] * (INTERVAL_MIN / 60)
    
    n_turbines = df["turbine_id"].nunique()
    total_energy = df["energy_kwh"].sum()
    
    time_span_hours = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 3600
    installed_kw = n_turbines * RATED_POWER_KW
    
    capacity_factor = total_energy / (installed_kw * time_span_hours) if time_span_hours > 0 else 0
    availability = 1 - (df["status_code"] == 2).mean()
    
    return {
        "n_turbines": n_turbines,
        "total_energy_kwh": total_energy,
        "capacity_factor": capacity_factor,
        "availability": availability,
        "hours": time_span_hours,
    }


def compute_turbine_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-turbine KPIs"""
    if df is None:
        return pd.DataFrame()
    
    df = df.copy()
    df["energy_kwh"] = df["power_kw"] * (INTERVAL_MIN / 60)
    hours = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 3600
    
    grouped = (
        df.groupby("turbine_id")
        .agg(
            energy_kwh=("energy_kwh", "sum"),
            fault_fraction=("status_code", lambda s: (s == 2).mean()),
            avg_power=("power_kw", "mean"),
            avg_wind_speed=("wind_speed", "mean"),
        )
        .reset_index()
    )
    
    grouped["capacity_factor"] = grouped["energy_kwh"] / (RATED_POWER_KW * hours)
    grouped["availability"] = 1 - grouped["fault_fraction"]
    
    return grouped.sort_values("capacity_factor", ascending=False)


def get_fault_summary(df: pd.DataFrame) -> dict:
    """Get fault count summary"""
    if df is None:
        return {}
    
    return df["diagnosis"].value_counts().to_dict()


def get_report_content() -> str:
    """Load report markdown content"""
    try:
        with open(REPORT_MD, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Report not generated yet. Run the AI pipeline first."

