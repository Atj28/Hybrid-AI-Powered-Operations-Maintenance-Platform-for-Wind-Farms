# 🌬️ Wind Farm AI Operator

**Hybrid AI-Powered Operations & Maintenance Platform for Wind Farms**

A comprehensive solution combining traditional analytics with AI-powered insights for wind turbine monitoring, fault diagnosis, predictive maintenance, and intelligent reporting.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Wind Farm AI Operator is a **hybrid AI system** that combines:

- **Rule-Based Analytics** - Deterministic fault detection using SCADA thresholds
- **LLM Intelligence** - GPT-4o-mini for natural language insights and recommendations
- **RAG (Retrieval Augmented Generation)** - Search OEM manuals for contextual troubleshooting
- **Multi-Agent Orchestration** - CrewAI for coordinated analysis pipeline
- **Interactive Dashboard** - Streamlit UI for real-time monitoring

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Performance Monitoring** | Farm & turbine KPIs, capacity factor, availability |
| **Fault Detection** | Gearbox, vibration, pitch, yaw, grid fault identification |
| **Troubleshooting** | AI-powered recommendations with manual references |
| **Predictive Maintenance** | Health scores, failure probability, maintenance scheduling |
| **Intelligent Reporting** | LLM-generated reports with executive summaries |
| **RAG Manual Search** | Search 1000+ pages of OEM documentation |

---

## ✨ Features

### 🤖 AI Pipeline (CrewAI)

Six specialized agents work together:

1. **Data Loader Agent** - Cleans and prepares SCADA data
2. **Performance Agent** - Computes KPIs and detects underperformance
3. **Fault Diagnosis Agent** - Identifies equipment faults
4. **Troubleshooting Agent** - Maps faults to maintenance actions (with RAG)
5. **Predictive Agent** - Calculates health scores and failure risks
6. **Reporting Agent** - Generates intelligent markdown/PDF reports

### 📊 Streamlit Dashboard

- **Dashboard** - Real-time farm overview with KPI gauges
- **Turbine Performance** - Individual turbine analysis and power curves
- **Fault Diagnosis** - Fault explorer with severity classification
- **AI Troubleshooting** - Chat interface with RAG-powered manual search
- **Predictive Maintenance** - Health scores and maintenance scheduling
- **Reports** - Generate and download intelligent reports

### 📚 RAG System

- **OpenAI Embeddings** - text-embedding-3-large for semantic search
- **ChromaDB** - Persistent vector storage
- **PDF Processing** - PyPDF loader for OEM manuals
- **Contextual Answers** - LLM responses grounded in documentation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WIND FARM AI OPERATOR                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │   SCADA     │    │    OEM      │    │   User      │                  │
│  │   Data      │    │  Manuals    │    │   Input     │                  │
│  │   (CSV)     │    │   (PDF)     │    │             │                  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                  │
│         │                  │                  │                          │
│         ▼                  ▼                  ▼                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     DATA LAYER                                   │    │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                    │    │
│  │  │  Parquet  │  │ ChromaDB  │  │   CSV     │                    │    │
│  │  │  (SCADA)  │  │  (RAG)    │  │ (Results) │                    │    │
│  │  └───────────┘  └───────────┘  └───────────┘                    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                           │
│                              ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   PROCESSING LAYER                               │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │  Rules   │  │   LLM    │  │   RAG    │  │  CrewAI  │        │    │
│  │  │  Engine  │  │ (GPT-4o) │  │  Search  │  │  Agents  │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                           │
│                              ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   PRESENTATION LAYER                             │    │
│  │                                                                  │    │
│  │  ┌──────────────────────┐  ┌──────────────────────┐             │    │
│  │  │   Streamlit Dashboard │  │   Reports (MD/PDF)   │             │    │
│  │  └──────────────────────┘  └──────────────────────┘             │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- OpenAI API Key
- ~2GB disk space (for PDFs and vector DB)

### Step 1: Clone Repository

```bash
git clone https://github.com/your-repo/wind_ai_operator.git
cd wind_ai_operator
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Add OEM Manuals (Optional but Recommended)

Place PDF manuals in `knowledge_base/` directory:

```
knowledge_base/
├── AWEA_OandM_Practices.pdf
├── Maintenance_Manual.pdf
└── Other_Manuals.pdf
```

### Step 6: Build RAG Database (If using manuals)

```bash
python -m src.rag.rag_build
```

---

## ⚡ Quick Start

### Option 1: Run Full AI Pipeline

```bash
cd src
python crew.py
```

This runs all 6 agents sequentially and generates reports.

### Option 2: Run Streamlit Dashboard

```bash
cd streamlit_app
streamlit run app.py
```

Open browser at `http://localhost:8501`

### Option 3: Run Individual Tools

```bash
# Clean SCADA data
python -c "from tools.data_loader import load_and_clean_data; load_and_clean_data()"

# Run performance analysis
python -c "from tools.performance_analyst import main; main()"

# Run fault diagnosis
python -c "from tools.fault_diagnosis import main; main()"

# Generate report
python -c "from tools.reporting import main; main(use_llm_insights=True)"
```

---

## 📁 Project Structure

```
wind_ai_operator/
│
├── 📂 data/                           # Data files
│   ├── wind_scada_5turbines_1month_realistic.csv  # Raw SCADA
│   ├── wind_scada_clean.parquet       # Cleaned data
│   ├── power_curve_empirical.csv      # Power curve
│   ├── underperformance_events.csv    # Underperformance
│   ├── fault_diagnosis_results.csv    # Fault detection
│   ├── troubleshooting_recommendations.csv
│   ├── turbine_health_scores.csv      # Health scores
│   └── wind_farm_intelligent_report.md  # Generated report
│
├── 📂 knowledge_base/                 # OEM PDF manuals
│   ├── AWEA-Operations-and-Maintenance.pdf
│   ├── Maintenance_Management_of_Wind_Turbines.pdf
│   └── Maintenance-manual.pdf
│
├── 📂 rag_db/                         # ChromaDB vector store
│
├── 📂 src/                            # Source code
│   ├── 📂 agents/                     # CrewAI agents
│   │   ├── data_loader_agent.py
│   │   ├── performance_agent.py
│   │   ├── fault_diagnosis_agent.py
│   │   ├── troubleshooting_agent.py
│   │   ├── predictive_agent.py
│   │   └── reporting_agent.py
│   │
│   ├── 📂 tools/                      # Tool implementations
│   │   ├── data_loader.py
│   │   ├── performance_analyst.py
│   │   ├── fault_diagnosis.py
│   │   ├── troubleshooting.py
│   │   ├── troubleshooting_knowledge.py  # Knowledge base
│   │   ├── predictive_maintainance.py
│   │   ├── reporting.py
│   │   ├── llm_insights.py            # LLM insight generators
│   │   └── search_manuals.py          # RAG search tool
│   │
│   ├── 📂 rag/                        # RAG system
│   │   ├── __init__.py
│   │   ├── rag_build.py               # Build vector DB
│   │   └── rag_loader.py              # Load & query
│   │
│   ├── tool.py                        # CrewAI tool definitions
│   ├── task.py                        # CrewAI task definitions
│   └── crew.py                        # Main pipeline
│
├── 📂 streamlit_app/                  # Dashboard
│   ├── app.py                         # Main entry
│   ├── 📂 pages/
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Turbine_Performance.py
│   │   ├── 3_Fault_Diagnosis.py
│   │   ├── 4_Troubleshooting_AI.py
│   │   ├── 5_Predictive_Maintenance.py
│   │   └── 6_Reports.py
│   ├── 📂 utils/
│   │   ├── load_data.py
│   │   ├── charts.py
│   │   ├── crew_runner.py
│   │   └── rag_query.py
│   └── 📂 config/
│       └── settings.py
│
├── .env                               # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📖 Usage Guide

### 1. Data Pipeline

The pipeline processes SCADA data through 6 stages:

```
Raw CSV → Clean Parquet → KPIs → Faults → Troubleshooting → Health → Report
```

**Run complete pipeline:**
```bash
cd src && python crew.py
```

### 2. Streamlit Dashboard

**Start dashboard:**
```bash
cd streamlit_app && streamlit run app.py
```

**Pages:**
- `/` - Landing page with navigation
- `/Dashboard` - Farm overview
- `/Turbine_Performance` - Individual turbine analysis
- `/Fault_Diagnosis` - Fault explorer
- `/Troubleshooting_AI` - AI chat with RAG
- `/Predictive_Maintenance` - Health scores
- `/Reports` - Generate/download reports

### 3. RAG Manual Search

**Build vector database (one-time):**
```bash
python -m src.rag.rag_build
```

**Query manuals programmatically:**
```python
from src.rag.rag_loader import search_manuals

results = search_manuals("How to change gearbox oil?")
print(results)
```

### 4. Generate Reports

**Basic template report:**
```python
from src.tools.reporting import main
main(use_llm_insights=False)
```

**Intelligent LLM report:**
```python
from src.tools.reporting import main
main(use_llm_insights=True)
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM and embeddings | Yes |
| `OPENAI_MODEL` | Model to use (default: gpt-4o-mini) | No |

### Thresholds (in `src/tools/`)

```python
# Fault detection thresholds
GEAR_OIL_TEMP_LIMIT = 85    # °C
NACELLE_TEMP_LIMIT = 70     # °C
VIB_HIGH_LIMIT = 1.5        # g-RMS
YAW_LIMIT = 15              # degrees
PITCH_STUCK_ANGLE = 0.5     # degrees

# Health score weights
OIL_SLOPE_LIMIT = 8         # °C/day
VIB_SLOPE_LIMIT = 0.4       # g/day
```

### RAG Settings (in `src/rag/rag_build.py`)

```python
# Chunk settings
CHUNK_SIZE = 1200           # tokens
CHUNK_OVERLAP = 200         # tokens

# Embedding model
EMBEDDING_MODEL = "text-embedding-3-large"

# Search settings
TOP_K = 4                   # results per query
```

---

## 🔌 API Reference

### Tools

| Tool | Function | Description |
|------|----------|-------------|
| `load_and_clean_scada_data` | `data_loader.load_and_clean_data()` | Clean raw SCADA CSV |
| `analyze_performance_and_kpis` | `performance_analyst.main()` | Compute KPIs |
| `diagnose_turbine_faults` | `fault_diagnosis.main()` | Detect faults |
| `generate_troubleshooting_recommendations` | `troubleshooting.main()` | Map faults to actions |
| `compute_health_scores` | `predictive_maintainance.run_predictive_agent()` | Calculate health |
| `generate_final_report` | `reporting.main()` | Create report |
| `search_manuals` | `rag_loader.search_manuals(query)` | RAG search |

### Data Files

| File | Format | Description |
|------|--------|-------------|
| `wind_scada_clean.parquet` | Parquet | Cleaned SCADA data |
| `power_curve_empirical.csv` | CSV | Wind speed vs power |
| `underperformance_events.csv` | CSV | Below-expected performance |
| `fault_diagnosis_results.csv` | CSV | Detected faults |
| `troubleshooting_recommendations.csv` | CSV | Fault → action mapping |
| `turbine_health_scores.csv` | CSV | Health scores 0-100 |
| `wind_farm_intelligent_report.md` | Markdown | Final report |

---

## 🧪 Testing

```bash
# Test RAG loader
python -m src.rag.rag_loader

# Test individual tools
python -c "from src.tools.data_loader import load_and_clean_data; load_and_clean_data()"
```

---

## 📊 Sample Output

### Health Scores
```
Turbine | Health Score | Status
--------|--------------|--------
T01     | 100          | 🟢 Good
T02     | 100          | 🟢 Good
T03     | 100          | 🟢 Good
T04     | 100          | 🟢 Good
T05     | 80           | 🟡 Warning
```

### Fault Summary
```
Diagnosis        | Count
-----------------|-------
NO_FAULT         | 22,127
GRID_EVENT       | 155
HIGH_VIBRATION   | 32
PITCH_STUCK      | 6
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**2. OpenAI API Error**
```bash
# Check .env file has valid API key
cat .env
```

**3. RAG Database Not Found**
```bash
python -m src.rag.rag_build
```

**4. Streamlit Port in Use**
```bash
streamlit run app.py --server.port 8502
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - LLM and embedding models
- **LangChain** - LLM orchestration framework
- **CrewAI** - Multi-agent framework
- **Streamlit** - Dashboard framework
- **ChromaDB** - Vector database

---

## 📞 Support

For questions or issues:
- Open a GitHub Issue
- Email: support@example.com

---

**Built with ❤️ for Wind Farm Operations**

