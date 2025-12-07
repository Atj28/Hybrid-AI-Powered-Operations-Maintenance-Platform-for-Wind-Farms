"""
Wind Farm AI Operator - Streamlit Dashboard
Main Entry Point
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Page configuration
st.set_page_config(
    page_title="Wind Farm AI Operator",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a5f7a;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .status-green { color: #28a745; font-weight: bold; }
    .status-yellow { color: #ffc107; font-weight: bold; }
    .status-red { color: #dc3545; font-weight: bold; }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<h1 class="main-header">🌬️ Wind Farm AI Operator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Hybrid AI-Powered Operations & Maintenance Platform</p>', unsafe_allow_html=True)
    
    # Divider
    st.divider()
    
    # Welcome Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### Welcome to the Wind Farm Intelligence Platform
        
        This platform combines **traditional analytics** with **AI-powered insights** to provide:
        
        - 📊 **Real-time Performance Monitoring**
        - ⚙️ **Per-Turbine Analysis & Benchmarking**  
        - 🚨 **Automated Fault Detection & Diagnosis**
        - 🔧 **AI-Powered Troubleshooting Recommendations**
        - 🧠 **Predictive Maintenance & Health Scoring**
        - 📝 **Intelligent Report Generation**
        """)
    
    st.divider()
    
    # Quick Navigation Cards
    st.markdown("### 🚀 Quick Navigation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>📊 Dashboard</h4>
            <p>Overview of farm performance, KPIs, and real-time status.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Dashboard", key="dash"):
            st.switch_page("pages/1_Dashboard.py")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>Fault Diagnosis</h4>
            <p>View detected faults, severity levels, and root causes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Fault Diagnosis", key="fault"):
            st.switch_page("pages/3_Fault_Diagnosis.py")
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4>Predictive Maintenance</h4>
            <p>Health scores and failure probability predictions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Predictions", key="pred"):
            st.switch_page("pages/5_Predictive_Maintenance.py")
    
    # Second row
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="card">
            <h4>Turbine Performance</h4>
            <p>Individual turbine analysis and power curves.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Performance", key="perf"):
            st.switch_page("pages/2_Turbine_Performance.py")
    
    with col5:
        st.markdown("""
        <div class="card">
            <h4>AI Troubleshooting</h4>
            <p>Get AI-powered recommendations for any issue.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Assistant", key="ai"):
            st.switch_page("pages/4_Troubleshooting_AI.py")
    
    with col6:
        st.markdown("""
        <div class="card">
            <h4>Reports</h4>
            <p>Generate and download intelligent reports.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Reports", key="rep"):
            st.switch_page("pages/6_Reports.py")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        <p>Powered by CrewAI + LangChain + Streamlit</p>
        <p>© 2024 Wind Farm AI Operator</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

