"""
AI Troubleshooting Page - Interactive AI Assistant with RAG
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.rag_query import (
    query_troubleshooting_ai, 
    get_fault_explanation,
    search_manuals_direct,
    get_available_manuals,
    is_rag_available
)
from utils.load_data import load_fault_diagnosis, get_fault_summary

st.set_page_config(page_title="AI Troubleshooting", page_icon="🔧", layout="wide")

st.title("🔧 AI Troubleshooting Assistant")
st.markdown("*Expert advice powered by OEM manuals and AI*")

# Check RAG availability
rag_available = is_rag_available()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with context and settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    use_rag = st.toggle("Use Manual Search (RAG)", value=rag_available, disabled=not rag_available)
    
    if not rag_available:
        st.warning("RAG database not found. Run:\n`python -m src.rag.rag_build`")
    else:
        st.success("RAG Database Active")
        
        # Show available manuals
        manuals = get_available_manuals()
        if manuals:
            with st.expander("📚 Available Manuals"):
                for manual in manuals:
                    st.markdown(f"- {manual}")
    
    st.divider()
    
    st.markdown("### 📋 Current Faults")
    
    fault_df = load_fault_diagnosis()
    if fault_df is not None:
        fault_summary = get_fault_summary(fault_df)
        faults = {k: v for k, v in fault_summary.items() if k != "NO_FAULT"}
        
        if faults:
            for fault, count in faults.items():
                st.markdown(f"- **{fault}**: {count}")
        else:
            st.success("No active faults")
    
    st.divider()
    
    st.markdown("### 💡 Quick Questions")
    
    quick_questions = [
        "What causes high vibration?",
        "Gearbox oil maintenance intervals?",
        "How to troubleshoot pitch faults?",
        "Safety checks before tower climb?",
        "Signs of bearing failure?",
    ]
    
    for q in quick_questions:
        if st.button(q, key=f"quick_{q[:20]}", use_container_width=True):
            st.session_state.quick_question = q

# Main content area - Tabs
tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📖 Manual Search", "🔍 Fault Lookup"])

# ============================================
# TAB 1: AI CHAT
# ============================================
with tab1:
    st.markdown("### Chat with AI Expert")
    
    if use_rag:
        st.info("🔍 RAG enabled - AI will search manuals for relevant context")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message.get("sources"):
                with st.expander("📚 Sources"):
                    for src in message["sources"]:
                        if "error" not in src:
                            st.markdown(f"- **{src['source']}**, Page {src['page']}")

    # Handle quick question
    if "quick_question" in st.session_state:
        prompt = st.session_state.quick_question
        del st.session_state.quick_question
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response with RAG
        with st.chat_message("assistant"):
            with st.spinner("Searching manuals and generating response..."):
                # Build context from current faults
                context = ""
                if fault_df is not None:
                    faults = {k: v for k, v in get_fault_summary(fault_df).items() if k != "NO_FAULT"}
                    if faults:
                        context = f"Currently detected faults: {faults}"
                
                response, sources = query_troubleshooting_ai(prompt, context, use_rag=use_rag)
                st.markdown(response)
                
                # Show sources
                if sources and not any("error" in s for s in sources):
                    with st.expander("📚 Manual Sources Referenced"):
                        for src in sources:
                            st.markdown(f"**{src['source']}** - Page {src['page']}")
                            st.caption(src.get('content', '')[:200] + "...")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "sources": sources
        })
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask about wind turbine maintenance..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response with RAG
        with st.chat_message("assistant"):
            with st.spinner("Searching manuals and generating response..."):
                context = ""
                if fault_df is not None:
                    faults = {k: v for k, v in get_fault_summary(fault_df).items() if k != "NO_FAULT"}
                    if faults:
                        context = f"Currently detected faults: {faults}"
                
                response, sources = query_troubleshooting_ai(prompt, context, use_rag=use_rag)
                st.markdown(response)
                
                if sources and not any("error" in s for s in sources):
                    with st.expander("📚 Manual Sources Referenced"):
                        for src in sources:
                            st.markdown(f"**{src['source']}** - Page {src['page']}")
                            st.caption(src.get('content', '')[:200] + "...")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "sources": sources
        })

    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# ============================================
# TAB 2: DIRECT MANUAL SEARCH
# ============================================
with tab2:
    st.markdown("### 📖 Search OEM Manuals")
    st.markdown("Search directly in the wind turbine manuals without AI interpretation.")
    
    if not rag_available:
        st.error("RAG database not available. Please build it first.")
    else:
        search_query = st.text_input("Enter search query:", placeholder="e.g., gearbox oil change procedure")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            num_results = st.selectbox("Results", [3, 5, 8, 10], index=1)
        
        if st.button("🔍 Search Manuals", type="primary"):
            if search_query:
                with st.spinner("Searching manuals..."):
                    results = search_manuals_direct(search_query, k=num_results)
                    
                    if results and "error" not in results[0]:
                        st.success(f"Found {len(results)} relevant sections")
                        
                        for i, result in enumerate(results, 1):
                            with st.expander(f"📄 Result {i}: {result['source']} (Page {result['page']})"):
                                st.markdown(f"**Relevance Score:** {1 - result['score']:.2%}")
                                st.divider()
                                st.markdown(result['content'])
                    else:
                        st.warning("No results found or error occurred.")
            else:
                st.warning("Please enter a search query.")

# ============================================
# TAB 3: FAULT LOOKUP
# ============================================
with tab3:
    st.markdown("### 🔍 Fault Type Lookup")
    st.markdown("Get detailed information about specific fault types from manuals.")
    
    fault_options = [
        "GEARBOX_OVERHEAT",
        "HIGH_VIBRATION",
        "PITCH_STUCK",
        "YAW_MISALIGNMENT",
        "GRID_EVENT",
        "BEARING_FAILURE",
        "BLADE_IMBALANCE",
        "CONVERTER_FAULT",
        "GENERATOR_OVERTEMP",
        "LOW_OIL_PRESSURE",
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_fault = st.selectbox("Select Fault Type", fault_options)
    
    with col2:
        use_rag_lookup = st.checkbox("Search manuals", value=rag_available, disabled=not rag_available)
    
    if st.button("📋 Get Fault Details", type="primary"):
        with st.spinner("Analyzing fault and searching manuals..."):
            response, sources = get_fault_explanation(selected_fault, use_rag=use_rag_lookup)
            
            st.markdown("### Analysis")
            st.markdown(response)
            
            if sources and not any("error" in s for s in sources):
                st.divider()
                st.markdown("### 📚 Manual References")
                for src in sources:
                    with st.expander(f"{src['source']} - Page {src['page']}"):
                        st.markdown(src.get('content', ''))

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    <p>Powered by RAG + GPT-4o-mini | Manual Knowledge Base</p>
</div>
""", unsafe_allow_html=True)
