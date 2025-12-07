"""
rag_loader.py
Load the persisted Chroma vector store built by rag_build.py

Usage:
    from src.rag.rag_loader import search_manuals
    
    results = search_manuals("What causes gearbox overheating?")
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_DIR = PROJECT_ROOT / "rag_db"

# Cached singleton
_vectordb = None


def load_manuals():
    """
    Load the existing Chroma DB from disk (rag_db/).
    Returns the vector store instance (cached).
    """
    global _vectordb
    
    if _vectordb is not None:
        return _vectordb
    
    if not DB_DIR.exists():
        raise FileNotFoundError(
            f"Vector DB directory '{DB_DIR}' not found. "
            f"Run 'python -m src.rag.rag_build' first to build it."
        )
    
    # Initialize embeddings (must match what was used in rag_build.py)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # Load persisted Chroma DB
    _vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )
    
    print(f"Loaded vector DB from {DB_DIR.resolve()}")
    print(f"Total vectors: {_vectordb._collection.count()}")
    
    return _vectordb


def search_manuals(query: str, k: int = 4) -> str:
    """
    Search the wind turbine manuals using RAG.
    
    Args:
        query: Natural language question about turbines, faults, maintenance
        k: Number of results to return (default 4)
    
    Returns:
        Formatted string with relevant passages from manuals
    """
    vectordb = load_manuals()
    
    # Perform similarity search
    results = vectordb.similarity_search(query, k=k)
    
    if not results:
        return "No relevant sections found in the manuals."
    
    # Format results with source citations
    chunks = []
    for i, doc in enumerate(results, start=1):
        meta = doc.metadata or {}
        source = meta.get("source", "unknown_source")
        page = meta.get("page", "?")
        
        chunks.append(
            f"[MANUAL EXCERPT {i}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{doc.page_content.strip()}\n"
        )
    
    return "\n" + "=" * 50 + "\n".join(chunks)


def search_manuals_with_scores(query: str, k: int = 4) -> list:
    """
    Search manuals and return results with similarity scores.
    
    Returns:
        List of (Document, score) tuples
    """
    vectordb = load_manuals()
    results = vectordb.similarity_search_with_score(query, k=k)
    return results


def get_manual_sources() -> list:
    """Get list of all unique source documents in the vector DB."""
    vectordb = load_manuals()
    
    # Get all documents metadata
    all_docs = vectordb._collection.get()
    
    sources = set()
    if all_docs and "metadatas" in all_docs:
        for meta in all_docs["metadatas"]:
            if meta and "source" in meta:
                sources.add(meta["source"])
    
    return sorted(list(sources))


# Test function
if __name__ == "__main__":
    print("Testing RAG Loader...")
    print("-" * 50)
    
    # List sources
    print("\nAvailable manual sources:")
    for src in get_manual_sources():
        print(f"  - {src}")
    
    # Test search
    test_query = "How to maintain gearbox oil in wind turbines?"
    print(f"\nTest query: {test_query}")
    print("-" * 50)
    
    result = search_manuals(test_query)
    print(result)

