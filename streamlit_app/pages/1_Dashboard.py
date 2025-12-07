"""
Dashboard Page - Wind Farm Overview
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import (
    load_scada_data, load_fault_diagnosis, load_health_scores,
    compute_farm_kpis, compute_turbine_kpis, get_fault_summary
)
from utils.charts import (
    create_kpi_gauge, create_turbine_comparison_bar,
    create_fault_distribution_pie, create_health_score_bar
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Wind Farm Dashboard")
st.markdown("*Real-time overview of farm performance and status*")

# Load data
scada_df = load_scada_data()
fault_df = load_fault_diagnosis()
health_df = load_health_scores()

if scada_df is not None:
    # Compute KPIs
    farm_kpis = compute_farm_kpis(scada_df)
    turbine_kpis = compute_turbine_kpis(scada_df)
    
    # Top KPI Row
    st.markdown("### 🎯 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Energy",
            value=f"{farm_kpis['total_energy_kwh']/1000:,.0f} MWh",
            delta=None
        )
    
    with col2:
        cf = farm_kpis['capacity_factor'] * 100
        st.metric(
            label="Capacity Factor",
            value=f"{cf:.1f}%",
            delta=f"{'Good' if cf > 30 else 'Low'}"
        )
    
    with col3:
        avail = farm_kpis['availability'] * 100
        st.metric(
            label="Availability",
            value=f"{avail:.1f}%",
            delta=f"{'Excellent' if avail > 98 else 'Check'}"
        )
    
    with col4:
        st.metric(
            label="Turbines",
            value=farm_kpis['n_turbines'],
            delta="Online"
        )
    
    st.divider()
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚡ Energy by Turbine")
        if not turbine_kpis.empty:
            fig = create_turbine_comparison_bar(
                turbine_kpis, "energy_kwh", "Energy (kWh)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏥 Health Scores")
        if health_df is not None:
            fig = create_health_score_bar(health_df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run predictive maintenance to see health scores.")
    
    st.divider()
    
    # Fault Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 Fault Distribution")
        if fault_df is not None:
            fault_summary = get_fault_summary(fault_df)
            fig = create_fault_distribution_pie(fault_summary)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run fault diagnosis to see fault distribution.")
    
    with col2:
        st.markdown("### 📋 Turbine Performance Ranking")
        if not turbine_kpis.empty:
            display_df = turbine_kpis[["turbine_id", "energy_kwh", "capacity_factor", "availability"]].copy()
            display_df["capacity_factor"] = (display_df["capacity_factor"] * 100).round(1).astype(str) + "%"
            display_df["availability"] = (display_df["availability"] * 100).round(1).astype(str) + "%"
            display_df["energy_kwh"] = display_df["energy_kwh"].round(0).astype(int)
            display_df.columns = ["Turbine", "Energy (kWh)", "CF", "Availability"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Recent Alerts
    st.markdown("### ⚠️ Recent Alerts")
    if fault_df is not None:
        recent_faults = fault_df[fault_df["diagnosis"] != "NO_FAULT"].tail(10)
        if not recent_faults.empty:
            st.dataframe(
                recent_faults[["timestamp", "turbine_id", "diagnosis"]].sort_values("timestamp", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No recent faults detected!")
    else:
        st.info("Run fault diagnosis to see alerts.")

else:
    st.warning("No SCADA data found. Please run the data pipeline first.")
    
    if st.button("🔄 Run Data Pipeline"):
        from utils.crew_runner import run_data_loader
        run_data_loader()
        st.rerun()

