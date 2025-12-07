from crewai import Agent
from tool import run_performance_analysis
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


PerformanceAgent = Agent(
    role="Performance Analyst",
    goal=(
        "Analyze wind farm performance, compute KPIs, and detect "
        "periods of underperformance versus expected power curves."
    ),
    backstory=(
        "You are a senior performance engineer with deep knowledge of "
        "capacity factor, availability, and turbine wake effects."
    ),
    tools=[run_performance_analysis],
    llm=llm_reasoning,
    verbose=True,
    allow_delegation=False,
)