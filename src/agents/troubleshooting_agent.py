from crewai import Agent
from tool import run_troubleshooting
from langchain_openai import ChatOpenAI 

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent directory)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# Add src to path for tool imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import RAG search tool (optional - may not be built yet)
try:
    from tools.search_manuals import search_manuals_tool
    rag_tools = [search_manuals_tool]
except Exception:
    rag_tools = []
    print("Note: RAG search_manuals tool not available. Run 'python -m src.rag.rag_build' to enable.")

llm_reasoning = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY"),
)

TroubleshootingAgent = Agent(
    role="Troubleshooting Specialist",
    goal=(
        "Given detected faults, consult OEM manuals and troubleshooting knowledge to "
        "explain likely root causes and recommend practical maintenance actions."
    ),
    backstory=(
        "You are a senior wind turbine field service engineer with 20+ years experience. "
        "You combine OEM manuals, troubleshooting guides, and field experience to provide "
        "actionable guidance to technicians. You always reference official documentation "
        "when available and prioritize safety."
    ),
    tools=[run_troubleshooting] + rag_tools,
    llm=llm_reasoning,
    verbose=True,
    allow_delegation=False,
)