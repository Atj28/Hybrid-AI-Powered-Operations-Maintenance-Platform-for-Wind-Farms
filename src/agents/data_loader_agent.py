from crewai import Agent
from tool import run_data_loader
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
DataLoaderAgent = Agent(
    role="Data Loader Agent",
    goal="Prepare a clean, analysis-ready SCADA dataset from raw files.",
    backstory=(
        "You specialize in handling noisy SCADA telemetry, "
        "ensuring timestamps, types, and missing values are correct."
    ),
    tools=[run_data_loader],
    llm=llm_calm,
    verbose=True,
    allow_delegation=False,
)
