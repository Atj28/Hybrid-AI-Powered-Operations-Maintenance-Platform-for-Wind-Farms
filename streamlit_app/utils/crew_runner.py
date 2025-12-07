"""
CrewAI Pipeline Runner for Wind Farm Dashboard
"""

import streamlit as st
from pathlib import Path
import sys
import subprocess


# Add src to path
SRC_DIR = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_DIR))


def run_full_pipeline():
    """Run the complete CrewAI pipeline"""
    try:
        # Import and run crew
        from crew import main as crew_main
        
        with st.spinner("Running AI Pipeline... This may take a few minutes."):
            crew_main()
        
        st.success("Pipeline completed successfully!")
        st.balloons()
        return True
        
    except Exception as e:
        st.error(f"Pipeline failed: {str(e)}")
        return False


def run_data_loader():
    """Run only the data loader step"""
    try:
        from tools.data_loader import load_and_clean_data
        
        with st.spinner("Loading and cleaning SCADA data..."):
            load_and_clean_data()
        
        st.success("Data loaded and cleaned!")
        return True
        
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        return False


def run_performance_analysis():
    """Run performance analysis step"""
    try:
        from tools.performance_analyst import main
        
        with st.spinner("Analyzing performance..."):
            main()
        
        st.success("Performance analysis complete!")
        return True
        
    except Exception as e:
        st.error(f"Performance analysis failed: {str(e)}")
        return False


def run_fault_diagnosis():
    """Run fault diagnosis step"""
    try:
        from tools.fault_diagnosis import main
        
        with st.spinner("Running fault diagnosis..."):
            main()
        
        st.success("Fault diagnosis complete!")
        return True
        
    except Exception as e:
        st.error(f"Fault diagnosis failed: {str(e)}")
        return False


def run_troubleshooting():
    """Run troubleshooting step"""
    try:
        from tools.troubleshooting import main
        
        with st.spinner("Generating troubleshooting recommendations..."):
            main()
        
        st.success("Troubleshooting complete!")
        return True
        
    except Exception as e:
        st.error(f"Troubleshooting failed: {str(e)}")
        return False


def run_predictive_maintenance():
    """Run predictive maintenance step"""
    try:
        from tools.predictive_maintainance import run_predictive_agent
        
        with st.spinner("Computing health scores..."):
            run_predictive_agent()
        
        st.success("Predictive maintenance complete!")
        return True
        
    except Exception as e:
        st.error(f"Predictive maintenance failed: {str(e)}")
        return False


def run_report_generation(use_llm: bool = True):
    """Run report generation step"""
    try:
        from tools.reporting import main
        
        with st.spinner("Generating intelligent report..."):
            main(use_llm_insights=use_llm)
        
        st.success("Report generated!")
        return True
        
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")
        return False


def get_pipeline_status() -> dict:
    """Check which pipeline outputs exist"""
    from config.settings import (
        SCADA_CLEAN, POWER_CURVE, UNDERPERF_EVENTS,
        FAULT_DIAGNOSIS, TROUBLESHOOTING, HEALTH_SCORES, REPORT_MD
    )
    
    return {
        "Data Cleaned": SCADA_CLEAN.exists(),
        "Performance Analyzed": POWER_CURVE.exists() and UNDERPERF_EVENTS.exists(),
        "Faults Diagnosed": FAULT_DIAGNOSIS.exists(),
        "Troubleshooting Ready": TROUBLESHOOTING.exists(),
        "Health Scores": HEALTH_SCORES.exists(),
        "Report Generated": REPORT_MD.exists(),
    }

