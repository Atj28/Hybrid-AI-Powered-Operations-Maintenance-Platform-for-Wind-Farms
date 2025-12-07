from crewai import Agent
from tool import run_fault_diagnosis
from langchain_openai import ChatOpenAI 

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent directory)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

llm_reasoning = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY"),
)


FaultDiagnosisAgent = Agent(
    role="Fault Diagnosis Agent",
    goal=(
        "Use SCADA-derived indicators and rule-based checks to detect "
        "gearbox, vibration, pitch, yaw, and grid-related faults."
    ),
    backstory=(
        "You have worked in wind turbine monitoring centers and can "
        "spot suspicious patterns quickly in fault diagnosis outputs."
    ),
    tools=[run_fault_diagnosis],
    llm=llm_reasoning,
    verbose=True,
    allow_delegation=False,
)
