from crewai import Agent
from tool import run_reporting
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

ReportingAgent = Agent(
    role="Reporting Agent",
    goal=(
        "Produce a concise but informative health report combining KPIs, "
        "faults, troubleshooting actions, and predictive scores."
    ),
    backstory=(
        "You act like a digital control-room analyst, summarizing "
        "the state of the wind farm for managers and engineers."
    ),
    tools=[run_reporting],
    llm=llm_reasoning,
    verbose=True,
    allow_delegation=False,
)
