# Sirex: Patient Medical Assistant

## Overview

**Sirex** is an AI-powered medical assistant designed to support patients throughout their healthcare journey. It provides symptom guidance, clinical record interaction, and actionable health insights through an interactive web interface.

---

## System Architecture

The project is structured into a modular pipeline combining data preprocessing, model inference, and frontend interaction:

```text
Sirex/
├── notebooks/          # Exploratory analysis, prompt testing, and prototyping
├── src/                # Core business logic, pipelines, agents, and data helpers
├── tests/              # Unit and integration test suites
├── Architecture.jpeg   # High-level system workflow diagram
├── app.py              # Web application entry point (Streamlit / Gradio / FastAPI UI)
├── main.py             # CLI pipeline runner or backend service entry point
├── pyproject.toml      # Project metadata, build system, and tool configs
└── requirements.txt    # Production and runtime Python dependencies

```

### High-Level Workflow

1. **User Query & Input Processing**: The patient enters symptoms, health questions, or uploads clinical notes/reports through the frontend (`app.py`).
2. **Context & Orchestration Layer (`src/`)**:
* Normalizes patient inputs and extracts key medical entities.
* Retrieves clinical knowledge bases or contextual medical guidelines.
* Evaluates queries through AI models/agents with medical safety guardrails.


3. **Inference & Response Formatting**: Generates calibrated, plain-language patient explanations, triage recommendations, and disclaimers.

---

## Installation & Setup

### Prerequisites

* Python 3.10 or higher
* `git` installed on your system

### 1. Clone the Repository

```bash
git clone https://github.com/Rajkumar-Ai-Engineer/Sirex.git
cd Sirex

```

### 2. Create and Activate a Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

*Alternatively, install in editable mode if packaging via `pyproject.toml`:*

```bash
pip install -e .

```

### 4. Environment Variables

Create a `.env` file in the project root to configure any required model API keys and service endpoints:

```env
OPENAI_API_KEY=your_openai_api_key_here
# or other LLM / vector store credentials as configured in src/
PORT=8000

```

---

## Usage Guide

### Running the Web Interface

Launch the primary patient assistant interface:

```bash
python app.py

```

*(If configured with Streamlit, run `streamlit run app.py`)*

### Running via CLI / Core Pipeline

Execute the main pipeline or batch processing tasks:

```bash
python main.py

```

### Running Tests

Execute the automated test suite to ensure system components and endpoints pass validation:

```bash
pytest tests/

```

---

## Key Modules & Responsibilities

* **`src/`**: Houses core algorithmic code, LLM orchestration, retriever logic, and safety guardrails.
* **`notebooks/`**: Dedicated sandbox for testing prompt variations, dataset evaluation, and exploratory model benchmarking.
* **`tests/`**: Contains regression tests for response integrity, input parsing, and pipeline orchestration.
* **`Architecture.jpeg`**: Visual reference detailing component interaction between the client, backend orchestrator, and AI services.

---

## Medical & Safety Disclaimer

> **Important**: Sirex is designed as an informational assistant and does not provide formal medical diagnoses, clinical prescriptions, or emergency healthcare services. Always seek the advice of a qualified healthcare provider for urgent or specific medical conditions.
