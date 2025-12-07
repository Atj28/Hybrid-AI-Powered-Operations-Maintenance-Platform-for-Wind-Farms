"""
Turbine Performance Page - Individual Turbine Analysis
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import load_scada_data, load_power_curve, compute_turbine_kpis
from utils.charts import create_power_curve, create_time_series, create_trend_line
from config.settings import TURBINE_IDS

st.set_page_config(page_title="Turbine Performance", page_icon="⚙️", layout="wide")

st.title("⚙️ Turbine Performance Analysis")
st.markdown("*Detailed performance metrics for individual turbines*")

# Load data
scada_df = load_scada_data()
power_curve_df = load_power_curve()

if scada_df is not None:
    # Turbine Selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_turbine = st.selectbox(
            "Select Turbine",
            options=["All Turbines"] + list(scada_df["turbine_id"].unique()),
            index=0
        )
    
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(scada_df["timestamp"].min().date(), scada_df["timestamp"].max().date()),
            key="date_range"
        )
    
    st.divider()
    
    # Filter data
    if selected_turbine != "All Turbines":
        filtered_df = scada_df[scada_df["turbine_id"] == selected_turbine].copy()
    else:
        filtered_df = scada_df.copy()
    
    # KPIs for selected turbine
    st.markdown(f"### 📊 Performance Metrics - {selected_turbine}")
    
    turbine_kpis = compute_turbine_kpis(filtered_df)
    
    if selected_turbine != "All Turbines" and not turbine_kpis.empty:
        t_data = turbine_kpis[turbine_kpis["turbine_id"] == selected_turbine].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Energy", f"{t_data['energy_kwh']/1000:,.1f} MWh")
        with col2:
            st.metric("Capacity Factor", f"{t_data['capacity_factor']*100:.1f}%")
        with col3:
            st.metric("Availability", f"{t_data['availability']*100:.1f}%")
        with col4:
            st.metric("Avg Power", f"{t_data['avg_power']:.0f} kW")
    
    st.divider()
    
    # Power Curve
    st.markdown("### 📈 Power Curve")
    
    turbine_for_curve = None if selected_turbine == "All Turbines" else selected_turbine
    fig = create_power_curve(filtered_df, turbine_for_curve)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Time Series Charts
    st.markdown("### 📉 Time Series Analysis")
    
    metric_options = ["power_kw", "wind_speed", "gear_oil_temp_c", "vibration_g_rms", "pitch_angle_deg", "yaw_misalignment_deg"]
    selected_metric = st.selectbox("Select Metric", metric_options, index=0)
    
    # Downsample for performance (only numeric columns)
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    display_df = filtered_df.set_index("timestamp")[numeric_cols].resample("1H").mean().reset_index()
    display_df["turbine_id"] = selected_turbine if selected_turbine != "All Turbines" else "Average"
    
    fig = create_time_series(display_df, selected_metric, f"{selected_metric} over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Detailed Trends (for single turbine)
    if selected_turbine != "All Turbines":
        st.markdown(f"### 🔍 Multi-Metric Trends - {selected_turbine}")
        
        metrics_to_show = ["power_kw", "gear_oil_temp_c", "vibration_g_rms"]
        
        fig = create_trend_line(filtered_df, selected_turbine, metrics_to_show)
        st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data Table
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            filtered_df.tail(100),
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning("No SCADA data found. Please run the data pipeline first.")

