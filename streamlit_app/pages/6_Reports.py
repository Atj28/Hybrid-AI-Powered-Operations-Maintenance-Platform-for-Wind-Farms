"""
Reports Page - Report Generation and Download
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.load_data import get_report_content
from utils.crew_runner import run_report_generation, get_pipeline_status
from config.settings import REPORT_MD, REPORT_PDF, DATA_DIR

st.set_page_config(page_title="Reports", page_icon="📝", layout="wide")

st.title("📝 Reports")
st.markdown("*Generate and download intelligent wind farm reports*")

# Pipeline Status
st.markdown("### 🔄 Pipeline Status")

status = get_pipeline_status()

col1, col2, col3 = st.columns(3)

for i, (step, completed) in enumerate(status.items()):
    col = [col1, col2, col3][i % 3]
    with col:
        if completed:
            st.success(f"✅ {step}")
        else:
            st.warning(f"⏳ {step}")

st.divider()

# Report Generation
st.markdown("### 📄 Generate Report")

col1, col2 = st.columns(2)

with col1:
    report_type = st.selectbox(
        "Report Type",
        options=["Intelligent Report (LLM-Enhanced)", "Basic Report (Template)"]
    )
    
    use_llm = "Intelligent" in report_type

with col2:
    if st.button("🚀 Generate Report", type="primary"):
        run_report_generation(use_llm=use_llm)
        st.rerun()

st.divider()

# Report Preview
st.markdown("### 📋 Report Preview")

report_content = get_report_content()

if "Report not generated" not in report_content:
    # Display report in tabs
    tab1, tab2 = st.tabs(["📄 Formatted View", "📝 Raw Markdown"])
    
    with tab1:
        st.markdown(report_content)
    
    with tab2:
        st.code(report_content, language="markdown")
    
    st.divider()
    
    # Download Options
    st.markdown("### 📥 Download Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Markdown download
        st.download_button(
            label="📄 Download Markdown",
            data=report_content,
            file_name="wind_farm_report.md",
            mime="text/markdown",
        )
    
    with col2:
        # PDF download (if exists)
        if REPORT_PDF.exists():
            with open(REPORT_PDF, "rb") as f:
                st.download_button(
                    label="📕 Download PDF",
                    data=f,
                    file_name="wind_farm_report.pdf",
                    mime="application/pdf",
                )
        else:
            st.info("PDF not available. Generate report to create PDF.")
    
    with col3:
        # HTML export
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Wind Farm Health Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 20px; }}
                h1 {{ color: #1a5f7a; border-bottom: 2px solid #1a5f7a; }}
                h2 {{ color: #2c7da0; }}
                h3 {{ color: #468faf; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #1a5f7a; color: white; }}
            </style>
        </head>
        <body>
            {report_content}
        </body>
        </html>
        """
        st.download_button(
            label="🌐 Download HTML",
            data=html_content,
            file_name="wind_farm_report.html",
            mime="text/html",
        )

else:
    st.info(report_content)
    
    if st.button("Generate First Report"):
        run_report_generation(use_llm=True)
        st.rerun()

st.divider()

# Historical Reports
st.markdown("### 📚 Available Reports")

report_files = list(DATA_DIR.glob("*.md")) + list(DATA_DIR.glob("*.pdf"))

if report_files:
    for report_file in sorted(report_files, reverse=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"📄 {report_file.name}")
        
        with col2:
            st.write(f"{report_file.stat().st_size / 1024:.1f} KB")
        
        with col3:
            if report_file.suffix == ".md":
                with open(report_file, "r") as f:
                    st.download_button(
                        "Download",
                        f.read(),
                        file_name=report_file.name,
                        key=f"dl_{report_file.name}"
                    )
            elif report_file.suffix == ".pdf":
                with open(report_file, "rb") as f:
                    st.download_button(
                        "Download",
                        f.read(),
                        file_name=report_file.name,
                        key=f"dl_{report_file.name}"
                    )
else:
    st.info("No reports generated yet.")

st.divider()

# Run Full Pipeline
st.markdown("### 🔄 Run Full AI Pipeline")

st.warning("This will run all 6 pipeline steps. It may take several minutes.")

if st.button("🚀 Run Complete AI Pipeline", type="secondary"):
    from utils.crew_runner import run_full_pipeline
    run_full_pipeline()
    st.rerun()

