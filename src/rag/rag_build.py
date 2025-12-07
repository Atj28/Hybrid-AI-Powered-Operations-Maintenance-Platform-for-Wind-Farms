"""
rag_build.py
Build and persist a Chroma vector store from PDFs in knowledge_base/

Run this ONCE to create the vector database:
    python -m src.rag.rag_build
    
Or from project root:
    cd /path/to/wind_ai_operator
    python src/rag/rag_build.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KB_DIR = PROJECT_ROOT / "knowledge_base"
DB_DIR = PROJECT_ROOT / "rag_db"


def load_all_pdfs():
    """Load all PDF documents from knowledge_base directory."""
    if not KB_DIR.exists():
        raise FileNotFoundError(f"knowledge_base directory not found: {KB_DIR}")
    
    docs = []
    pdf_files = list(KB_DIR.glob("*.pdf"))
    
    if not pdf_files:
        raise RuntimeError("No PDF documents found in knowledge_base/")
    
    print(f"\nFound {len(pdf_files)} PDF files in {KB_DIR}")
    print("-" * 50)
    
    for pdf in pdf_files:
        print(f"Loading: {pdf.name}")
        try:
            loader = PyPDFLoader(str(pdf))
            pdf_docs = loader.load()
            
            # Add source metadata
            for d in pdf_docs:
                d.metadata["source"] = pdf.name
            
            docs.extend(pdf_docs)
            print(f"  -> Loaded {len(pdf_docs)} pages")
            
        except Exception as e:
            print(f"  -> ERROR loading {pdf.name}: {e}")
    
    print("-" * 50)
    print(f"Total pages loaded: {len(docs)}")
    return docs


def split_docs(docs):
    """Split documents into chunks for embedding."""
    print("\nSplitting documents into chunks...")
    
    # Good defaults for technical manuals
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
        length_function=len,
    )
    
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")
    
    # Show sample chunk info
    if chunks:
        avg_len = sum(len(c.page_content) for c in chunks) / len(chunks)
        print(f"Average chunk size: {avg_len:.0f} characters")
    
    return chunks


def build_vector_db(chunks):
    """Create embeddings and store in ChromaDB."""
    print("\nCreating embeddings with OpenAI (text-embedding-3-large)...")
    print("This may take a few minutes for large documents...")
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # Create Chroma vector store
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
    )
    
    # Persist to disk
    vectordb.persist()
    
    print(f"\nVector DB built and saved to: {DB_DIR.resolve()}")
    print(f"Total vectors stored: {vectordb._collection.count()}")
    
    return vectordb


def test_search(vectordb):
    """Test the vector DB with a sample query."""
    print("\n" + "=" * 50)
    print("Testing vector DB with sample query...")
    print("=" * 50)
    
    test_query = "What are the common causes of gearbox failure in wind turbines?"
    results = vectordb.similarity_search(test_query, k=2)
    
    print(f"\nQuery: {test_query}")
    print(f"\nTop {len(results)} results:")
    
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        content = doc.page_content[:200] + "..."
        print(f"\n[Result {i}] Source: {source}, Page: {page}")
        print(f"Content: {content}")


def main():
    """Main function to build the RAG vector database."""
    print("=" * 50)
    print("RAG Vector Database Builder")
    print("Wind Turbine Manual Knowledge Base")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables!")
    
    # Load PDFs
    docs = load_all_pdfs()
    
    # Split into chunks
    chunks = split_docs(docs)
    
    # Build vector DB
    vectordb = build_vector_db(chunks)
    
    # Test search
    test_search(vectordb)
    
    print("\n" + "=" * 50)
    print("RAG Vector Database build complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()

