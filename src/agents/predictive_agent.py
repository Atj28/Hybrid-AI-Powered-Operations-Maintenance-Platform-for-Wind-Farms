from crewai import Agent
from tool import run_predictive
from langchain_openai import ChatOpenAI 

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent directory)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

llm_calm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    api_key=os.getenv("OPENAI_API_KEY"),
)

PredictiveAgent = Agent(
    role="Predictive Maintenance Agent",
    goal=(
        "Analyze trends in temperature, vibration, and performance "
        "to compute health scores and identify early-risk turbines."
    ),
    backstory=(
        "You are focused on anticipating failures days or weeks before "
        "they happen using trend analysis."
    ),
    tools=[run_predictive],
    llm=llm_calm,
    verbose=True,
    allow_delegation=False,
)