"""
search_manuals.py
CrewAI tool for searching OEM manuals and troubleshooting PDFs using RAG.
"""

from crewai.tools import tool
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@tool("search_manuals")
def search_manuals_tool(query: str) -> str:
    """
    Search wind turbine OEM manuals and troubleshooting PDFs using RAG.
    
    Use this tool when you need to:
    - Find maintenance procedures from official manuals
    - Look up troubleshooting steps for specific faults
    - Get technical specifications or guidelines
    - Reference OEM recommendations
    
    Args:
        query: Natural language question about wind turbine maintenance,
               faults, troubleshooting, or technical specifications.
    
    Returns:
        Relevant passages from the manuals with source citations.
    
    Example queries:
        - "What are the maintenance intervals for gearbox oil?"
        - "How to troubleshoot high vibration in main bearing?"
        - "What causes pitch system faults?"
        - "Safety procedures for tower climb"
    """
    try:
        from rag.rag_loader import search_manuals
        
        result = search_manuals(query, k=4)
        return result
        
    except FileNotFoundError as e:
        return (
            "RAG database not found. Please run 'python -m src.rag.rag_build' "
            "to build the vector database from PDF manuals first."
        )
    except Exception as e:
        return f"Error searching manuals: {str(e)}"


# Standalone function for non-CrewAI usage
def query_manuals(query: str, k: int = 4) -> str:
    """
    Standalone function to query manuals (for Streamlit integration).
    """
    try:
        from rag.rag_loader import search_manuals
        return search_manuals(query, k=k)
    except Exception as e:
        return f"Error: {str(e)}"

