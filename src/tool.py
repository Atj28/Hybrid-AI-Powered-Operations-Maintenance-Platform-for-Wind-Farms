# tools.py
# ---------------------------------------------------------
# This file defines ALL CrewAI tools used by your agents.
# Each tool wraps one of your pipeline steps (1 → 6).
# ---------------------------------------------------------

from crewai.tools import tool
from tools import data_loader, performance_analyst, fault_diagnosis, troubleshooting, predictive_maintainance, reporting

# -----------------------------
# STEP 1 — DATA LOADER
# -----------------------------
@tool("load_and_clean_scada_data")
def run_data_loader():
    """
    Loads raw SCADA data, cleans it, interpolates missing values,
    converts dtypes, and saves wind_scada_clean.parquet.
    
    This tool prepares the SCADA dataset for analysis.
    """
    data_loader.load_and_clean_data()
    return "Step 1 complete: SCADA cleaned and saved."


# -----------------------------
# STEP 2 — PERFORMANCE ANALYSIS
# -----------------------------
@tool("analyze_performance_and_kpis")
def run_performance_analysis():
    """
    Runs performance analysis on cleaned SCADA data.
    
    Outputs:
    - Farm and per-turbine KPIs
    - Empirical power curve (power_curve_empirical.csv)
    - Underperformance events (underperformance_events.csv)
    """
    performance_analyst.main()
    return "Step 2 complete: KPIs, power curve, underperformance saved."


# -----------------------------
# STEP 3 — FAULT DIAGNOSIS
# -----------------------------
@tool("diagnose_turbine_faults")
def run_fault_diagnosis():
    """
    Runs rule-based fault diagnosis on SCADA data.
    
    Detects:
    - Gearbox overheating
    - High vibration
    - Pitch stuck faults
    - Yaw misalignment
    - Grid events
    
    Outputs: fault_diagnosis_results.csv
    """
    fault_diagnosis.main()
    return "Step 3 complete: Fault diagnosis saved."


# -----------------------------
# STEP 4 — TROUBLESHOOTING (Mini-RAG)
# -----------------------------
@tool("generate_troubleshooting_recommendations")
def run_troubleshooting():
    """
    Maps detected faults to troubleshooting recommendations.
    
    Adds:
    - Fault descriptions
    - Probable causes
    - Recommended actions
    - Severity levels
    
    Outputs: troubleshooting_recommendations.csv
    """
    troubleshooting.main()
    return "Step 4 complete: Troubleshooting recommendations saved."


# -----------------------------
# STEP 5 — PREDICTIVE MAINTENANCE
# -----------------------------
@tool("compute_health_scores")
def run_predictive():
    """
    Runs predictive maintenance analysis.
    
    Computes:
    - Rolling trends for temperature and vibration
    - Abnormal slope detection
    - Health score for each turbine (0-100)
    
    Outputs: turbine_health_scores.csv
    """
    predictive_maintainance.run_predictive_agent()
    return "Step 5 complete: Health scores saved."


# -----------------------------
# STEP 6 — REPORT GENERATION
# -----------------------------
@tool("generate_final_report")
def run_reporting():
    """
    Generates the final wind farm health report with LLM-enhanced insights.
    
    Each specialist team contributes:
    - Performance Engineering: KPIs, efficiency analysis, recommendations
    - Reliability Engineering: Fault patterns, risk assessment, root causes
    - Field Service: Troubleshooting guide, maintenance priorities
    - Predictive Analytics: Health scores, failure predictions, scheduling
    
    The report includes an executive summary synthesizing all insights.
    
    Outputs: wind_farm_intelligent_report.md (Markdown format with AI analysis)
    """
    reporting.main(use_llm_insights=True)
    return "Step 6 complete: Intelligent report with LLM insights generated."
