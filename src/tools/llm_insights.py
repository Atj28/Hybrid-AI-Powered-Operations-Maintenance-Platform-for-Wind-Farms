# llm_insights.py
# ---------------------------------------------------------
# LLM-powered insight generation for each specialist agent.
# Each function analyzes data and provides expert-level insights.
# ---------------------------------------------------------

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# Initialize LLM for insights
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


# ==========================================================
# 1. PERFORMANCE ANALYST INSIGHTS
# ==========================================================
def generate_performance_insights(farm_kpis: dict, per_turbine_kpis, underperf_count: int) -> str:
    """
    Generate expert performance analysis insights.
    Think like: Senior Performance Engineer
    """
    llm = get_llm()
    
    prompt = f"""You are a Senior Wind Farm Performance Engineer analyzing monthly SCADA data.

## Data Summary:
- Number of Turbines: {farm_kpis['n_turbines']}
- Total Energy Generated: {farm_kpis['total_energy_kwh']:.2f} kWh
- Farm Capacity Factor: {farm_kpis['capacity_factor']*100:.2f}%
- Farm Availability: {farm_kpis['availability']*100:.2f}%
- Underperformance Events Detected: {underperf_count}

## Per-Turbine Performance:
{per_turbine_kpis.to_string()}

## Your Analysis Tasks:
1. **Performance Assessment**: Rate overall farm performance (Excellent/Good/Fair/Poor)
2. **Top Performer**: Identify best performing turbine and explain why
3. **Underperformer**: Identify worst performing turbine and possible reasons
4. **Energy Loss Analysis**: Estimate energy losses from underperformance
5. **Recommendations**: 2-3 specific actions to improve performance

Write in professional technical language. Be specific with numbers.
"""
    
    response = llm.invoke(prompt)
    return response.content


# ==========================================================
# 2. FAULT DIAGNOSIS INSIGHTS  
# ==========================================================
def generate_fault_diagnosis_insights(fault_summary: dict, total_records: int) -> str:
    """
    Generate expert fault diagnosis insights.
    Think like: Reliability Engineer / Condition Monitoring Specialist
    """
    llm = get_llm()
    
    # Format fault summary
    fault_text = "\n".join([f"- {fault}: {count} events" for fault, count in fault_summary.items()])
    
    prompt = f"""You are a Wind Turbine Reliability Engineer analyzing fault diagnosis results.

## Data Summary:
- Total SCADA Records Analyzed: {total_records}
- Monitoring Period: 1 Month

## Fault Distribution:
{fault_text}

## Your Analysis Tasks:
1. **Risk Assessment**: Rate overall turbine health risk (Low/Medium/High/Critical)
2. **Priority Faults**: Rank faults by severity and urgency
3. **Root Cause Hypothesis**: For each fault type, suggest likely root causes
4. **Pattern Analysis**: Note any concerning patterns or trends
5. **Immediate Actions**: What should O&M team do this week?

Write like a professional reliability report. Focus on actionable insights.
"""
    
    response = llm.invoke(prompt)
    return response.content


# ==========================================================
# 3. TROUBLESHOOTING SPECIALIST INSIGHTS
# ==========================================================
def generate_troubleshooting_insights(fault_types: list, severity_distribution: dict) -> str:
    """
    Generate expert troubleshooting recommendations.
    Think like: Field Service Engineer / OEM Technical Support
    """
    llm = get_llm()
    
    prompt = f"""You are a Wind Turbine Field Service Engineer providing troubleshooting guidance.

## Detected Fault Types:
{', '.join(fault_types)}

## Severity Distribution:
- Critical: {severity_distribution.get('CRITICAL', 0)} events
- High: {severity_distribution.get('HIGH', 0)} events  
- Medium: {severity_distribution.get('MEDIUM', 0)} events
- Low: {severity_distribution.get('LOW to MEDIUM', 0) + severity_distribution.get('LOW', 0)} events

## Your Analysis Tasks:
1. **Priority Work Orders**: List top 3 issues requiring immediate field visits
2. **Safety Considerations**: Any safety protocols to follow?
3. **Tools & Parts**: What should technicians bring for site visits?
4. **Escalation Path**: When should OEM support be contacted?
5. **Preventive Actions**: How to prevent these issues in future?

Write practical, field-ready guidance. Think like you're briefing technicians.
"""
    
    response = llm.invoke(prompt)
    return response.content


# ==========================================================
# 4. PREDICTIVE MAINTENANCE INSIGHTS
# ==========================================================
def generate_predictive_insights(health_scores: dict, trend_data: dict) -> str:
    """
    Generate predictive maintenance insights.
    Think like: Predictive Maintenance Analyst / Data Scientist
    """
    llm = get_llm()
    
    # Format health scores
    health_text = "\n".join([f"- {tid}: Health Score {score:.0f}/100" for tid, score in health_scores.items()])
    
    prompt = f"""You are a Predictive Maintenance Analyst using SCADA trend analysis.

## Turbine Health Scores (0-100):
{health_text}

## Trend Indicators:
- Oil Temperature Trending: {trend_data.get('oil_trend', 'Normal')}
- Vibration Trending: {trend_data.get('vib_trend', 'Normal')}
- Yaw System Status: {trend_data.get('yaw_status', 'Normal')}

## Your Analysis Tasks:
1. **Failure Risk Ranking**: Rank turbines by failure probability (next 30 days)
2. **Early Warning Signs**: What deterioration patterns do you see?
3. **Remaining Useful Life**: Estimate time before maintenance needed
4. **Maintenance Schedule**: Prioritize upcoming inspections
5. **Cost Avoidance**: Estimate cost savings from predictive actions

Use probabilistic language where appropriate. Focus on forward-looking insights.
"""
    
    response = llm.invoke(prompt)
    return response.content


# ==========================================================
# 5. REPORTING AGENT - EXECUTIVE SUMMARY
# ==========================================================
def generate_executive_summary(
    performance_insights: str,
    fault_insights: str, 
    troubleshooting_insights: str,
    predictive_insights: str,
    farm_kpis: dict
) -> str:
    """
    Generate executive summary combining all specialist insights.
    Think like: Wind Farm Manager / Asset Manager
    """
    llm = get_llm()
    
    prompt = f"""You are a Wind Farm Asset Manager preparing a monthly operations report for senior management.

## Farm Overview:
- Turbines: {farm_kpis['n_turbines']}
- Energy: {farm_kpis['total_energy_kwh']:.0f} kWh
- Capacity Factor: {farm_kpis['capacity_factor']*100:.1f}%
- Availability: {farm_kpis['availability']*100:.1f}%

## Performance Engineer's Analysis:
{performance_insights}

---

## Reliability Engineer's Analysis:
{fault_insights}

---

## Field Service Engineer's Recommendations:
{troubleshooting_insights}

---

## Predictive Maintenance Analysis:
{predictive_insights}

---

## Your Task - Write Executive Summary:

Create a professional 1-page executive summary that includes:

1. **Overall Status** (🟢 Green / 🟡 Yellow / 🔴 Red)
2. **Key Metrics This Month** (3-4 bullet points)
3. **Critical Issues Requiring Attention** (prioritized list)
4. **Maintenance Actions Scheduled** (next 7 days)
5. **Cost & Risk Implications**
6. **Management Recommendations**

Write for executives - concise, actionable, business-focused.
Use emojis sparingly for status indicators.
"""
    
    response = llm.invoke(prompt)
    return response.content


# ==========================================================
# 6. FULL REPORT BUILDER
# ==========================================================
def build_intelligent_report(
    farm_kpis: dict,
    per_turbine_kpis,
    fault_summary: dict,
    health_data,
    underperf_count: int
) -> str:
    """
    Build complete intelligent report with all specialist insights.
    """
    print("Generating Performance Insights...")
    perf_insights = generate_performance_insights(farm_kpis, per_turbine_kpis, underperf_count)
    
    print("Generating Fault Diagnosis Insights...")
    fault_insights = generate_fault_diagnosis_insights(fault_summary, sum(fault_summary.values()))
    
    print("Generating Troubleshooting Insights...")
    # Get unique fault types (excluding NO_FAULT)
    fault_types = [f for f in fault_summary.keys() if f != "NO_FAULT"]
    severity_dist = {"HIGH": fault_summary.get("HIGH_VIBRATION", 0) + fault_summary.get("GEARBOX_OVERHEAT", 0),
                     "CRITICAL": fault_summary.get("PITCH_STUCK", 0),
                     "MEDIUM": fault_summary.get("YAW_MISALIGNMENT", 0),
                     "LOW to MEDIUM": fault_summary.get("GRID_EVENT", 0)}
    troubleshoot_insights = generate_troubleshooting_insights(fault_types, severity_dist)
    
    print("Generating Predictive Maintenance Insights...")
    health_scores = dict(zip(health_data["turbine_id"], health_data["health_score"]))
    trend_data = {"oil_trend": "Normal", "vib_trend": "Monitoring", "yaw_status": "Normal"}
    predictive_insights = generate_predictive_insights(health_scores, trend_data)
    
    print("Generating Executive Summary...")
    exec_summary = generate_executive_summary(
        perf_insights, fault_insights, troubleshoot_insights, predictive_insights, farm_kpis
    )
    
    # Build final report
    report_lines = []
    report_lines.append("# Wind Farm Intelligent Health Report")
    report_lines.append("")
    report_lines.append("*Generated by Hybrid AI Operator System with LLM-Enhanced Analysis*")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Executive Summary (First!)
    report_lines.append("## Executive Summary")
    report_lines.append("")
    report_lines.append(exec_summary)
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Performance Analysis
    report_lines.append("## Performance Analysis")
    report_lines.append("*By: Performance Engineering Team*")
    report_lines.append("")
    report_lines.append(perf_insights)
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Fault Diagnosis
    report_lines.append("## Fault Diagnosis Report")
    report_lines.append("*By: Reliability Engineering Team*")
    report_lines.append("")
    report_lines.append(fault_insights)
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Troubleshooting
    report_lines.append("## 🔧 Troubleshooting & Field Service Guide")
    report_lines.append("*By: Field Service Engineering Team*")
    report_lines.append("")
    report_lines.append(troubleshoot_insights)
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Predictive Maintenance
    report_lines.append("## Predictive Maintenance Analysis")
    report_lines.append("*By: Predictive Analytics Team*")
    report_lines.append("")
    report_lines.append(predictive_insights)
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Raw Data Summary
    report_lines.append("## Raw Data Summary")
    report_lines.append("")
    report_lines.append(f"| Metric | Value |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Total Turbines | {farm_kpis['n_turbines']} |")
    report_lines.append(f"| Total Energy (kWh) | {farm_kpis['total_energy_kwh']:,.0f} |")
    report_lines.append(f"| Capacity Factor | {farm_kpis['capacity_factor']*100:.1f}% |")
    report_lines.append(f"| Availability | {farm_kpis['availability']*100:.1f}% |")
    report_lines.append(f"| Underperformance Events | {underperf_count} |")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("*Report generated automatically. For questions, contact Operations Center.*")
    
    return "\n".join(report_lines)

