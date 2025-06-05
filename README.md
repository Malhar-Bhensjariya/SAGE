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
│   ├── flask_app/
│   │   ├── agents/                          # Core AI agents
│   │   │   ├── supervisor_agent.py
│   │   │   ├── research_agent.py
│   │   │   ├── summarizer_agent.py
│   │   │   ├── critique_agent.py
│   │   │   └── strategy_agent.py
│   │   ├── core/
│   │   │   ├── routes/
│   │   │   │   ├── user_routes.py
│   │   │   │   ├── task_routes.py
│   │   │   │   └── document_routes.py
│   │   │   ├── services/
│   │   │   │   ├── agent_service.py
│   │   │   │   ├── planning_service.py
│   │   │   │   └── rag_service.py            # Logic for RAG + CAG
│   │   │   └── utils/
│   │   │       ├── memory.py
│   │   │       ├── logger.py
│   │   │       ├── file_parser.py            # PDF/DOC parsing
│   │   │       └── text_splitter.py          # Chunking logic
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   └── db_init.py
│   │   ├── data/
│   │   │   ├── memory/                       # JSON or SQLite memory
│   │   │   │   └── task_context.json
│   │   │   └── uploaded/                     # Uploaded PDFs/DOCs
│   │   ├── config/
│   │   │   ├── settings.py
│   │   │   └── secrets_template.env
│   │   ├── tools/                            # External API connectors
│   │   │   ├── gemini_connector.py
│   │   │   └── serpapi_connector.py
│   │   ├── app.py
│   │   └── requirements.txt

│   └── postgres/
│       ├── init.sql
│       └── docker-compose.yml

├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── AgentCard.jsx
│   │   │   ├── TaskTimeline.jsx
│   │   │   └── UploadBox.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Agents.jsx
│   │   │   ├── ExploreDoc.jsx                # For RAG/CAG UI
│   │   │   └── Dashboard.jsx
│   │   ├── hooks/
│   │   │   └── useUploadTask.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── taskService.js
│   │   │   └── docService.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── vite.config.js
│   └── package.json

├── .env
├── .gitignore
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
```
### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## Agent Overview
- Agent	Responsibility
- Supervisor	Manages goals, context, and agent coordination
- Research Agent	Pulls data from APIs or datasets
- Summarizer	Converts findings into digestible insights
- Critique Agent	Detects gaps, bias, or flaws in logic
- Strategy Agent	Suggests next steps based on task state
