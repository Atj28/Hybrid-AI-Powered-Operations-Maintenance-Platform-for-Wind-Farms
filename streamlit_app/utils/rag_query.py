"""
RAG Query Module for AI-Powered Troubleshooting
Integrates with ChromaDB vector store of wind turbine manuals
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import sys

# Add src to path for RAG imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Load environment
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)


def get_llm():
    """Get LLM instance for chat"""
    try:
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    except Exception as e:
        st.error(f"Failed to initialize LLM: {e}")
        return None


def get_rag_context(query: str, k: int = 4) -> tuple:
    """
    Get RAG context from wind turbine manuals.
    
    Returns:
        tuple: (context_string, list_of_sources)
    """
    try:
        from rag.rag_loader import search_manuals, search_manuals_with_scores
        
        # Get results with scores
        results = search_manuals_with_scores(query, k=k)
        
        if not results:
            return "", []
        
        # Format context
        context_parts = []
        sources = []
        
        for doc, score in results:
            meta = doc.metadata or {}
            source = meta.get("source", "Unknown Manual")
            page = meta.get("page", "?")
            
            context_parts.append(
                f"[From: {source}, Page {page}]\n{doc.page_content.strip()}"
            )
            sources.append({
                "source": source,
                "page": page,
                "score": float(score),
                "content": doc.page_content[:300] + "..."
            })
        
        context = "\n\n---\n\n".join(context_parts)
        return context, sources
        
    except FileNotFoundError:
        return "", [{"error": "RAG database not built. Run: python -m src.rag.rag_build"}]
    except Exception as e:
        return "", [{"error": str(e)}]


def query_troubleshooting_ai(question: str, context: str = "", use_rag: bool = True) -> tuple:
    """
    Query the AI for troubleshooting advice with optional RAG context.
    
    Args:
        question: User's question
        context: Optional context about current faults/issues
        use_rag: Whether to search manuals for context
    
    Returns:
        tuple: (AI response string, list of sources used)
    """
    llm = get_llm()
    if llm is None:
        return "LLM not available. Please check your API key.", []
    
    # Get RAG context if enabled
    rag_context = ""
    sources = []
    
    if use_rag:
        rag_context, sources = get_rag_context(question)
    
    # Build prompt with wind turbine expertise
    system_prompt = """You are an expert Wind Turbine Field Service Engineer with 20+ years of experience.
You have access to official OEM manuals and maintenance documentation.

Your expertise includes:
- Wind turbine mechanical systems (gearbox, bearings, blades, main shaft)
- Electrical systems (generator, converter, transformer, grid connection)
- Control systems (pitch, yaw, SCADA, PLC)
- Hydraulic and lubrication systems
- Predictive maintenance and condition monitoring
- Safety protocols and OEM procedures

When answering:
1. Reference the manual excerpts provided when relevant
2. Be specific and actionable with step-by-step procedures
3. Include safety considerations and warnings
4. Mention relevant tools, parts, or equipment needed
5. Indicate when to escalate to OEM support
6. Cite the source manual and page when referencing documentation
"""

    # Build user prompt with context
    user_parts = []
    
    if rag_context:
        user_parts.append(f"RELEVANT MANUAL EXCERPTS:\n{rag_context}\n")
    
    if context:
        user_parts.append(f"CURRENT SITUATION:\n{context}\n")
    
    user_parts.append(f"QUESTION:\n{question}\n")
    user_parts.append("\nProvide a detailed, practical answer. Reference the manual excerpts where applicable.")
    
    user_prompt = "\n".join(user_parts)

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm.invoke(messages)
        return response.content, sources
        
    except Exception as e:
        return f"Error querying AI: {str(e)}", sources


def search_manuals_direct(query: str, k: int = 4) -> list:
    """
    Direct manual search without LLM - just RAG retrieval.
    
    Returns:
        List of search results with source info
    """
    try:
        from rag.rag_loader import search_manuals_with_scores
        
        results = search_manuals_with_scores(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            meta = doc.metadata or {}
            formatted_results.append({
                "source": meta.get("source", "Unknown"),
                "page": meta.get("page", "?"),
                "score": float(score),
                "content": doc.page_content.strip()
            })
        
        return formatted_results
        
    except FileNotFoundError:
        return [{"error": "RAG database not found. Run: python -m src.rag.rag_build"}]
    except Exception as e:
        return [{"error": str(e)}]


def get_fault_explanation(fault_type: str, use_rag: bool = True) -> tuple:
    """Get detailed explanation for a fault type using RAG."""
    
    query = f"""
    Explain the fault type: {fault_type}
    
    Please provide:
    1. What this fault means and how it's detected
    2. Common root causes
    3. Immediate actions to take
    4. Long-term solutions and repairs
    5. How to prevent it in the future
    6. Safety considerations
    """
    
    return query_troubleshooting_ai(query, use_rag=use_rag)


def analyze_turbine_health(turbine_id: str, health_score: float, 
                           metrics: dict, use_rag: bool = True) -> tuple:
    """Get AI analysis of turbine health with RAG context."""
    
    query = f"""
    Analyze turbine health and provide maintenance recommendations.
    
    Turbine: {turbine_id}
    Health Score: {health_score}/100
    
    Current Metrics:
    - Oil Temperature: {metrics.get('oil_temp', 'N/A')}°C
    - Vibration: {metrics.get('vibration', 'N/A')} g-RMS
    - Yaw Misalignment: {metrics.get('yaw', 'N/A')}°
    
    Based on these metrics and OEM guidelines, provide:
    1. Overall health assessment
    2. Specific concerns and risk factors
    3. Recommended maintenance actions (with procedures from manuals)
    4. Estimated time until maintenance required
    5. Cost-saving opportunities through predictive maintenance
    """
    
    return query_troubleshooting_ai(query, use_rag=use_rag)


def get_available_manuals() -> list:
    """Get list of available manuals in the RAG database."""
    try:
        from rag.rag_loader import get_manual_sources
        return get_manual_sources()
    except:
        return []


def is_rag_available() -> bool:
    """Check if RAG database is available."""
    rag_db_path = PROJECT_ROOT / "rag_db"
    return rag_db_path.exists() and any(rag_db_path.iterdir())
