"""
Fault Diagnosis Page - Fault Detection and Analysis
Enhanced with beautiful AI explanation display
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import load_fault_diagnosis, load_troubleshooting, get_fault_summary
from utils.charts import create_fault_distribution_pie
from utils.rag_query import get_fault_explanation, is_rag_available
from config.settings import SEVERITY_COLORS

st.set_page_config(page_title="Fault Diagnosis", page_icon="🚨", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .fault-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #e94560;
    }
    .fault-header {
        color: #e94560;
        font-size: 1.4em;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .section-card {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .section-title {
        color: #00d9ff;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .source-card {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border-radius: 8px;
        padding: 12px;
        margin: 5px 0;
        border-left: 3px solid #00d9ff;
    }
    .source-title {
        color: #00d9ff;
        font-size: 0.9em;
        font-weight: 600;
    }
    .source-page {
        color: #ffd700;
        font-size: 0.85em;
    }
    .source-preview {
        color: #a0a0a0;
        font-size: 0.8em;
        margin-top: 5px;
    }
    .severity-critical { color: #ff4444; font-weight: bold; }
    .severity-high { color: #ff8c00; font-weight: bold; }
    .severity-medium { color: #ffd700; font-weight: bold; }
    .severity-low { color: #00d9ff; font-weight: bold; }
    .rag-badge {
        background: linear-gradient(90deg, #00d9ff, #0f3460);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)


def format_ai_explanation(explanation: str, sources: list, fault_type: str):
    """Format AI explanation with beautiful styling."""
    
    # Header
    st.markdown(f"""
    <div class="fault-card">
        <div class="fault-header">
            🔍 AI Analysis: {fault_type}
            <span class="rag-badge">RAG-Enhanced</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse explanation into sections
    sections = parse_explanation_sections(explanation)
    
    # Display each section in an expander
    section_icons = {
        "what": "📋",
        "causes": "⚠️",
        "immediate": "🚨",
        "long-term": "🔧",
        "prevent": "🛡️",
        "safety": "⚡"
    }
    
    section_titles = {
        "what": "What This Fault Means",
        "causes": "Common Root Causes", 
        "immediate": "Immediate Actions",
        "long-term": "Long-Term Solutions",
        "prevent": "Prevention Strategies",
        "safety": "Safety Considerations"
    }
    
    col1, col2 = st.columns(2)
    
    sections_list = list(sections.items())
    
    for i, (key, content) in enumerate(sections_list):
        icon = section_icons.get(key, "📌")
        title = section_titles.get(key, key.title())
        
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            with st.expander(f"{icon} {title}", expanded=(i < 2)):
                st.markdown(content)
    
    # Sources section
    if sources and not any("error" in s for s in sources if isinstance(s, dict)):
        st.markdown("---")
        st.markdown("### 📚 Manual References")
        
        cols = st.columns(min(len(sources), 4))
        
        for i, source in enumerate(sources):
            if isinstance(source, dict) and "error" not in source:
                with cols[i % 4]:
                    source_name = Path(source.get("source", "Unknown")).stem[:30]
                    page = source.get("page", "?")
                    score = source.get("score", 0)
                    preview = source.get("content", "")[:150] + "..."
                    
                    # Relevance indicator
                    if score > 1.0:
                        relevance = "🟢 High"
                    elif score > 0.8:
                        relevance = "🟡 Medium"
                    else:
                        relevance = "🔵 Related"
                    
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-title">📄 {source_name}</div>
                        <div class="source-page">Page {page} • {relevance}</div>
                        <div class="source-preview">{preview}</div>
                    </div>
                    """, unsafe_allow_html=True)


def parse_explanation_sections(explanation: str) -> dict:
    """Parse the AI explanation into structured sections."""
    sections = {}
    
    # Common section patterns
    patterns = [
        ("what", ["what this fault means", "what this means", "1.", "definition"]),
        ("causes", ["common root causes", "root causes", "causes", "2."]),
        ("immediate", ["immediate actions", "immediate steps", "3."]),
        ("long-term", ["long-term", "long term", "solutions", "repairs", "4."]),
        ("prevent", ["prevent", "prevention", "future", "5."]),
        ("safety", ["safety", "6."])
    ]
    
    lines = explanation.split('\n')
    current_section = "overview"
    current_content = []
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if this line starts a new section
        section_found = None
        for section_key, keywords in patterns:
            if any(kw in line_lower for kw in keywords):
                section_found = section_key
                break
        
        if section_found and section_found != current_section:
            # Save previous section
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            current_section = section_found
            current_content = [line]
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    # If no sections found, return as single overview
    if len(sections) <= 1:
        sections = {"overview": explanation}
    
    return sections


def get_severity_for_fault(fault_type: str) -> tuple:
    """Get severity level and color for a fault type."""
    severity_map = {
        "GEARBOX_OVERHEAT": ("CRITICAL", "#ff4444"),
        "HIGH_VIBRATION": ("HIGH", "#ff8c00"),
        "PITCH_STUCK": ("HIGH", "#ff8c00"),
        "YAW_MISALIGN": ("MEDIUM", "#ffd700"),
        "GRID_EVENT": ("MEDIUM", "#ffd700"),
        "NO_FAULT": ("NONE", "#00d9ff"),
    }
    return severity_map.get(fault_type, ("UNKNOWN", "#a0a0a0"))


# Main Page Content
st.title("🚨 Fault Diagnosis")
st.markdown("*AI-powered fault detection and root cause analysis*")

# RAG Status indicator
if is_rag_available():
    st.success("✅ RAG Manual Search: Active (3 OEM manuals loaded)")
else:
    st.warning("⚠️ RAG not available. Run `python -m src.rag.rag_build` for enhanced analysis.")

# Load data
fault_df = load_fault_diagnosis()
trouble_df = load_troubleshooting()

if fault_df is not None:
    # Summary Stats
    st.markdown("### 📊 Fault Summary")
    
    fault_summary = get_fault_summary(fault_df)
    total_faults = sum(v for k, v in fault_summary.items() if k != "NO_FAULT")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(fault_df):,}")
    with col2:
        st.metric("Fault Events", f"{total_faults:,}")
    with col3:
        st.metric("Fault Rate", f"{total_faults/len(fault_df)*100:.2f}%")
    with col4:
        unique_faults = len([k for k in fault_summary if k != "NO_FAULT" and fault_summary[k] > 0])
        st.metric("Fault Types", unique_faults)
    
    st.divider()
    
    # Fault Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Fault Distribution")
        fig = create_fault_distribution_pie(fault_summary)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Fault Counts by Type")
        
        # Enhanced fault counts with severity colors
        fault_data = []
        for k, v in fault_summary.items():
            severity, color = get_severity_for_fault(k)
            fault_data.append({
                "Fault Type": k,
                "Count": v,
                "Percentage": f"{v/len(fault_df)*100:.2f}%",
                "Severity": severity
            })
        
        fault_counts_df = pd.DataFrame(fault_data).sort_values("Count", ascending=False)
        
        st.dataframe(
            fault_counts_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Severity": st.column_config.TextColumn(
                    "Severity",
                    help="Fault severity level"
                )
            }
        )
    
    st.divider()
    
    # Fault Explorer with AI Analysis
    st.markdown("### 🔍 Fault Explorer & AI Analysis")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        fault_types = [k for k in fault_summary.keys() if k != "NO_FAULT" and fault_summary[k] > 0]
        if fault_types:
            selected_fault = st.selectbox(
                "Select Fault Type",
                fault_types,
                help="Choose a fault type to analyze"
            )
        else:
            selected_fault = None
            st.info("🎉 No faults detected in the data!")
    
    with col2:
        turbine_filter = st.selectbox(
            "Filter by Turbine",
            options=["All"] + sorted(list(fault_df["turbine_id"].unique())),
            help="Filter events by turbine"
        )
    
    with col3:
        if selected_fault:
            severity, severity_color = get_severity_for_fault(selected_fault)
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 8px; background: {severity_color}20; 
                        border-left: 4px solid {severity_color}; margin-top: 25px;">
                <strong style="color: {severity_color};">Severity: {severity}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    if selected_fault:
        # Filter data
        filtered = fault_df[fault_df["diagnosis"].str.contains(selected_fault, na=False)]
        if turbine_filter != "All":
            filtered = filtered[filtered["turbine_id"] == turbine_filter]
        
        # Event count
        st.markdown(f"**📍 Found {len(filtered):,} events for `{selected_fault}`**")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Recent Events", "🤖 AI Analysis", "📊 Time Distribution"])
        
        with tab1:
            # Show recent events
            display_cols = ["timestamp", "turbine_id", "diagnosis", "power_kw", "wind_speed"]
            available_cols = [c for c in display_cols if c in filtered.columns]
            
            st.dataframe(
                filtered[available_cols].tail(20).sort_values("timestamp", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            # AI Explanation with enhanced display
            st.markdown("#### 🤖 AI-Powered Fault Analysis")
            st.caption("Uses RAG to search OEM manuals and provide expert-level analysis")
            
            if st.button(f"🔍 Analyze {selected_fault}", type="primary", use_container_width=True):
                with st.spinner("🔄 Searching manuals and generating analysis..."):
                    try:
                        result = get_fault_explanation(selected_fault)
                        
                        # Handle both tuple (explanation, sources) and string returns
                        if isinstance(result, tuple):
                            explanation, sources = result
                        else:
                            explanation = result
                            sources = []
                        
                        # Display formatted explanation
                        format_ai_explanation(explanation, sources, selected_fault)
                        
                        # Store in session state for persistence
                        st.session_state[f"analysis_{selected_fault}"] = {
                            "explanation": explanation,
                            "sources": sources
                        }
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
            
            # Show cached analysis if available
            elif f"analysis_{selected_fault}" in st.session_state:
                cached = st.session_state[f"analysis_{selected_fault}"]
                format_ai_explanation(
                    cached["explanation"],
                    cached["sources"],
                    selected_fault
                )
        
        with tab3:
            # Time distribution chart
            if "timestamp" in filtered.columns:
                st.markdown("#### 📈 Fault Events Over Time")
                
                time_df = filtered.copy()
                time_df["date"] = pd.to_datetime(time_df["timestamp"]).dt.date
                daily_counts = time_df.groupby("date").size().reset_index(name="count")
                
                st.bar_chart(daily_counts.set_index("date"))
    
    st.divider()
    
    # Troubleshooting Recommendations
    if trouble_df is not None:
        st.markdown("### 🔧 Troubleshooting Recommendations")
        
        # Show unique recommendations
        if "fault_description" in trouble_df.columns:
            unique_recs = trouble_df[trouble_df["diagnosis"] != "NO_FAULT"][
                ["diagnosis", "fault_description", "fault_severity", "recommended_actions"]
            ].drop_duplicates()
            
            for _, row in unique_recs.iterrows():
                severity_color = SEVERITY_COLORS.get(row["fault_severity"], "#6c757d")
                
                with st.expander(f"🔹 {row['diagnosis']} - Severity: {row['fault_severity']}"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 8px; 
                                    background: {severity_color}20; 
                                    border-left: 4px solid {severity_color};">
                            <strong>Severity:</strong> {row['fault_severity']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"**Description:** {row['fault_description']}")
                    
                    st.markdown("**Recommended Actions:**")
                    for i, action in enumerate(row["recommended_actions"].split(" | "), 1):
                        st.markdown(f"{i}. {action.strip()}")
        else:
            st.info("Run troubleshooting pipeline to see recommendations.")

else:
    st.warning("⚠️ No fault diagnosis data found. Please run the pipeline first.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Run Fault Diagnosis Pipeline", type="primary"):
            from utils.crew_runner import run_fault_diagnosis
            with st.spinner("Running fault diagnosis..."):
                run_fault_diagnosis()
            st.rerun()
    
    with col2:
        st.info("💡 This will analyze SCADA data and detect turbine faults.")
