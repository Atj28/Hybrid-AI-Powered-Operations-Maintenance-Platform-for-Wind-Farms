from crewai import Task 


from agents.data_loader_agent import DataLoaderAgent
from agents.performance_agent import PerformanceAgent
from agents.fault_diagnosis_agent import FaultDiagnosisAgent
from agents.troubleshooting_agent import TroubleshootingAgent
from agents.predictive_agent import PredictiveAgent
from agents.reporting_agent import ReportingAgent


data_loader_task = Task(
    description=(
        "Run the SCADA data loading and cleaning pipeline. "
        "Ensure the cleaned file wind_scada_clean.parquet exists in the data folder."
    ),
    expected_output="A cleaned SCADA dataset stored as wind_scada_clean.parquet.",
    agent=DataLoaderAgent,
)

performance_task = Task(
    description=(
        "Run the performance analysis pipeline on the cleaned SCADA data. "
        "Compute farm and per-turbine KPIs, generate the empirical power curve, "
        "and detect underperformance. Ensure power_curve_empirical.csv and "
        "underperformance_events.csv are created."
    ),
    expected_output=(
        "Performance KPIs computed and underperformance_events.csv created in the data folder."
    ),
    agent=PerformanceAgent,
)

fault_task = Task(
    description=(
        "Run the fault diagnosis pipeline to inspect SCADA and underperformance events. "
        "Identify gear, vibration, pitch, yaw, and grid-related issues. "
        "Save the full results as fault_diagnosis_results.csv."
    ),
    expected_output="Fault diagnosis results saved as fault_diagnosis_results.csv.",
    agent=FaultDiagnosisAgent,
)

troubleshooting_task = Task(
    description=(
        "Using the fault_diagnosis_results.csv, call the troubleshooting pipeline and "
        "use the 'search_manuals' tool when helpful to consult OEM manuals. "
        "Generate troubleshooting_recommendations.csv that includes explanations, "
        "severity, and recommended actions for each turbine and time period."
    ),
    expected_output="Troubleshooting recommendations saved as troubleshooting_recommendations.csv.",
    agent=TroubleshootingAgent,
)

predictive_task = Task(
    description=(
        "Run the predictive maintenance pipeline using the cleaned SCADA data. "
        "Compute trend-based health scores for each turbine and save them as "
        "turbine_health_scores.csv."
    ),
    expected_output="Health scores saved as turbine_health_scores.csv.",
    agent=PredictiveAgent,
)

report_task = Task(
    description=(
        "Generate a final wind farm health report by combining KPIs, fault diagnosis, "
        "troubleshooting actions, and predictive health scores. "
        "Save the report as wind_farm_health_report.md in the data folder."
    ),
    expected_output="Markdown report file wind_farm_health_report.md created.",
    agent=ReportingAgent,
)

