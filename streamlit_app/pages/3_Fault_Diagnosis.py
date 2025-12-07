"""
Fault Diagnosis Page - Fault Detection and Analysis
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import load_fault_diagnosis, load_troubleshooting, get_fault_summary
from utils.charts import create_fault_distribution_pie
from utils.rag_query import get_fault_explanation
from config.settings import SEVERITY_COLORS

st.set_page_config(page_title="Fault Diagnosis", page_icon="🚨", layout="wide")

st.title("🚨 Fault Diagnosis")
st.markdown("*Automated fault detection and root cause analysis*")

# Load data
fault_df = load_fault_diagnosis()
trouble_df = load_troubleshooting()

if fault_df is not None:
    # Summary Stats
    st.markdown("### 📊 Fault Summary")
    
    fault_summary = get_fault_summary(fault_df)
    total_faults = sum(v for k, v in fault_summary.items() if k != "NO_FAULT")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(fault_df))
    with col2:
        st.metric("Fault Events", total_faults)
    with col3:
        st.metric("Fault Rate", f"{total_faults/len(fault_df)*100:.2f}%")
    with col4:
        st.metric("Fault Types", len([k for k in fault_summary if k != "NO_FAULT"]))
    
    st.divider()
    
    # Fault Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Fault Distribution")
        fig = create_fault_distribution_pie(fault_summary)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Fault Counts")
        fault_counts_df = pd.DataFrame([
            {"Fault Type": k, "Count": v, "Percentage": f"{v/len(fault_df)*100:.2f}%"}
            for k, v in fault_summary.items()
        ]).sort_values("Count", ascending=False)
        st.dataframe(fault_counts_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Fault Explorer
    st.markdown("### 🔍 Fault Explorer")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fault_types = [k for k in fault_summary.keys() if k != "NO_FAULT"]
        if fault_types:
            selected_fault = st.selectbox("Select Fault Type", fault_types)
        else:
            selected_fault = None
            st.info("No faults detected!")
    
    with col2:
        turbine_filter = st.selectbox(
            "Filter by Turbine",
            options=["All"] + list(fault_df["turbine_id"].unique())
        )
    
    if selected_fault:
        # Filter data
        filtered = fault_df[fault_df["diagnosis"].str.contains(selected_fault, na=False)]
        if turbine_filter != "All":
            filtered = filtered[filtered["turbine_id"] == turbine_filter]
        
        st.markdown(f"**Found {len(filtered)} events for {selected_fault}**")
        
        # Show recent events
        st.dataframe(
            filtered[["timestamp", "turbine_id", "diagnosis", "power_kw", "wind_speed"]].tail(20).sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # AI Explanation
        st.markdown("### 🤖 AI Fault Explanation")
        
        if st.button(f"Get AI Analysis for {selected_fault}"):
            with st.spinner("Analyzing fault..."):
                explanation = get_fault_explanation(selected_fault)
                st.markdown(explanation)
    
    st.divider()
    
    # Troubleshooting Recommendations
    if trouble_df is not None:
        st.markdown("### 🔧 Troubleshooting Recommendations")
        
        # Show unique recommendations
        if "fault_description" in trouble_df.columns:
            unique_recs = trouble_df[trouble_df["diagnosis"] != "NO_FAULT"][
                ["diagnosis", "fault_description", "fault_severity", "recommended_actions"]
            ].drop_duplicates()
            
            for _, row in unique_recs.iterrows():
                severity_color = SEVERITY_COLORS.get(row["fault_severity"], "#6c757d")
                
                with st.expander(f"🔹 {row['diagnosis']} - Severity: {row['fault_severity']}"):
                    st.markdown(f"**Description:** {row['fault_description']}")
                    st.markdown(f"**Recommended Actions:**")
                    for action in row["recommended_actions"].split(" | "):
                        st.markdown(f"- {action}")
    else:
        st.info("Run troubleshooting pipeline to see recommendations.")

else:
    st.warning("No fault diagnosis data found. Please run the pipeline first.")
    
    if st.button("🔄 Run Fault Diagnosis"):
        from utils.crew_runner import run_fault_diagnosis
        run_fault_diagnosis()
        st.rerun()

