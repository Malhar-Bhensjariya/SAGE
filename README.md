# SAGE – Multi-Agent AI System with a Supervisory Agent for Guided Exploration

**SAGE** (Supervisory Agent for Guided Exploration) is a modular multi-agent AI system designed to solve real-world problems that current single-agent LLMs cannot handle well. A central Supervisor Agent manages specialized sub-agents (research, summarization, critique, planning) to perform context-aware, multi-step tasks across sessions.

Built entirely with free tools (Gemini 2.0 flash, PostgreSQL, Flask, React, etc.), SAGE enables scalable, persistent, and intelligent workflows for research, analysis, and learning.

---

## Features

- **Persistent Context & Memory:** Tasks are tracked over time using JSON/SQLite/PostgreSQL.
- **Agent Specialization:** Each sub-agent focuses on a domain (e.g., research, critique, summarization).
- **Long-Term Planning:** The Supervisor Agent coordinates goals, checkpoints, and next steps.
- **Cross-Domain Execution:** Research, analysis, summarization, and strategy in one workflow.
- **Adaptive Learning Paths:** Ideal for intelligent tutoring systems or knowledge exploration.
- **Fully Modular:** Agents can be swapped or extended independently.

---

## Project Structure
```text
sage/
├── backend/
│ ├── flask_app/ # Flask API + Sub-agent logic + Memory handling
│ └── postgres/ # PostgreSQL schema + Docker DB setup
├── frontend/ # ReactJS + TailwindCSS user interface
├── .env # Environment variables (Git-ignored)
└── README.md
```

**Highlights:**
- `flask_app/agents/` – Agent implementations (research, summarize, etc.)
- `flask_app/core/` – Routes, services, and utility logic
- `data/memory/` – Persistent task context (JSON or SQLite fallback)
- `frontend/src/components/` – UI components for interacting with SAGE

---

## Setup Instructions

### Backend (Flask + PostgreSQL)
Flask Setup:
```bash
cd backend/flask_app
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
Setup DB (optional if using SQLite)
```bash
cd ../postgres
docker-compose up -d
Run Flask App
# From flask_app/
python app.py
Frontend (React + TailwindCSS)
```
### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

##Agent Overview
- Agent	Responsibility
- Supervisor	Manages goals, context, and agent coordination
- Research Agent	Pulls data from APIs or datasets
- Summarizer	Converts findings into digestible insights
- Critique Agent	Detects gaps, bias, or flaws in logic
- Strategy Agent	Suggests next steps based on task state
