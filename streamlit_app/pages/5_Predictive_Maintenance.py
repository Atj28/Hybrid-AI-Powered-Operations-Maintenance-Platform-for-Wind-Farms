"""
Predictive Maintenance Page - Health Scores and Predictions
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import load_health_scores, load_scada_data
from utils.charts import create_health_score_bar, create_trend_line
from utils.rag_query import analyze_turbine_health
from config.settings import STATUS_COLORS

st.set_page_config(page_title="Predictive Maintenance", page_icon="🧠", layout="wide")

st.title("🧠 Predictive Maintenance")
st.markdown("*AI-powered health monitoring and failure prediction*")

# Load data
health_df = load_health_scores()
scada_df = load_scada_data()

if health_df is not None:
    # Summary Stats
    st.markdown("### 📊 Fleet Health Overview")
    
    avg_health = health_df["health_score"].mean()
    min_health = health_df["health_score"].min()
    at_risk = len(health_df[health_df["health_score"] < 80])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        color = STATUS_COLORS["green"] if avg_health >= 80 else STATUS_COLORS["yellow"] if avg_health >= 50 else STATUS_COLORS["red"]
        st.metric("Average Health", f"{avg_health:.0f}/100")
    
    with col2:
        st.metric("Minimum Health", f"{min_health:.0f}/100")
    
    with col3:
        st.metric("Turbines At Risk", at_risk)
    
    with col4:
        st.metric("Healthy Turbines", len(health_df) - at_risk)
    
    st.divider()
    
    # Health Score Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🏥 Health Scores by Turbine")
        fig = create_health_score_bar(health_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Health Details")
        display_df = health_df.copy()
        display_df["health_score"] = display_df["health_score"].astype(int)
        
        # Add status indicator
        def get_status(score):
            if score >= 80:
                return "🟢 Good"
            elif score >= 50:
                return "🟡 Warning"
            else:
                return "🔴 Critical"
        
        display_df["Status"] = display_df["health_score"].apply(get_status)
        
        st.dataframe(
            display_df[["turbine_id", "health_score", "Status"]].sort_values("health_score"),
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()
    
    # Detailed Analysis
    st.markdown("### 🔍 Detailed Turbine Analysis")
    
    selected_turbine = st.selectbox(
        "Select Turbine for Analysis",
        options=health_df["turbine_id"].tolist()
    )
    
    if selected_turbine:
        turbine_data = health_df[health_df["turbine_id"] == selected_turbine].iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Health Score", f"{turbine_data['health_score']:.0f}")
        with col2:
            st.metric("Oil Temp", f"{turbine_data.get('oil_temp', 'N/A')}°C")
        with col3:
            st.metric("Oil Slope", f"{turbine_data.get('oil_slope', 'N/A'):.2f}°C/day")
        with col4:
            st.metric("Vibration", f"{turbine_data.get('vibration', 'N/A'):.2f} g")
        with col5:
            st.metric("Yaw", f"{turbine_data.get('yaw', 'N/A'):.1f}°")
        
        # AI Analysis
        st.markdown("### 🤖 AI Health Analysis")
        
        if st.button("Generate AI Analysis"):
            with st.spinner("Analyzing turbine health..."):
                metrics = {
                    "oil_temp": turbine_data.get("oil_temp", "N/A"),
                    "vibration": turbine_data.get("vibration", "N/A"),
                    "yaw": turbine_data.get("yaw", "N/A"),
                }
                analysis = analyze_turbine_health(
                    selected_turbine,
                    turbine_data["health_score"],
                    metrics
                )
                st.markdown(analysis)
        
        # Trend Analysis
        if scada_df is not None:
            st.markdown("### 📈 Historical Trends")
            
            metrics_to_show = ["gear_oil_temp_c", "vibration_g_rms", "power_kw"]
            fig = create_trend_line(scada_df, selected_turbine, metrics_to_show)
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Maintenance Schedule
    st.markdown("### 📅 Recommended Maintenance Schedule")
    
    schedule_data = []
    for _, row in health_df.iterrows():
        if row["health_score"] < 50:
            priority = "Immediate"
            timeframe = "Within 7 days"
        elif row["health_score"] < 80:
            priority = "Soon"
            timeframe = "Within 30 days"
        else:
            priority = "Routine"
            timeframe = "Within 90 days"
        
        schedule_data.append({
            "Turbine": row["turbine_id"],
            "Health": row["health_score"],
            "Priority": priority,
            "Timeframe": timeframe,
            "Action": "Inspection" if row["health_score"] >= 80 else "Maintenance"
        })
    
    schedule_df = pd.DataFrame(schedule_data).sort_values("Health")
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

else:
    st.warning("No health scores found. Please run the predictive maintenance pipeline.")
    
    if st.button("🔄 Run Predictive Maintenance"):
        from utils.crew_runner import run_predictive_maintenance
        run_predictive_maintenance()
        st.rerun()

