from crewai import Crew

# Import all agents
from agents.data_loader_agent import DataLoaderAgent
from agents.performance_agent import PerformanceAgent
from agents.fault_diagnosis_agent import FaultDiagnosisAgent
from agents.troubleshooting_agent import TroubleshootingAgent
from agents.predictive_agent import PredictiveAgent
from agents.reporting_agent import ReportingAgent

# Import all tasks
from task import (
    data_loader_task,
    performance_task,
    fault_task,
    troubleshooting_task,
    predictive_task,
    report_task,
)


# Create the crew
wind_ai_operator_crew = Crew(
    agents=[
        DataLoaderAgent,
        PerformanceAgent,
        FaultDiagnosisAgent,
        TroubleshootingAgent,
        PredictiveAgent,
        ReportingAgent,
    ],
    tasks=[
        data_loader_task,
        performance_task,
        fault_task,
        troubleshooting_task,
        predictive_task,
        report_task,
    ],
    verbose=True,
)


def main():
    print("Starting Hybrid Wind AI Operator (LLM + RAG + Tools)...")
    result = wind_ai_operator_crew.kickoff()
    print("\n Pipeline finished. Final crew result:")
    print(result)
    print("\nCheck the data/ folder for generated CSVs and the Markdown report.")


if __name__ == "__main__":
    main()
