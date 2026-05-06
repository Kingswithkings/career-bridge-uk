CareerBridge UK 🇬🇧

AI-powered career mentor for international students and migrants in the UK.

🚀 Features

- AI CV Analyzer
- UK-standard CV Generator
- Job Match Engine
- Interview Preparation Engine
- AI Mock Interview (real-time feedback)

🧠 Tech Stack

- Frontend: Streamlit
- Backend: FastAPI
- AI: OpenAI
- Database: PostgreSQL (planned)

📦 Project Structure

- backend/ → API + AI logic
- frontend/ → Streamlit app
- docs/ → PRD and documentation

🎯 Goal

Help users go from:

CV → Job → Interview → Offer

🛠️ Local Setup

Docker is not required for local development. Use the Python virtualenvs:

Backend:

```bash
cd /Users/1stkings/Careerbridge-uk
backend/.venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd /Users/1stkings/Careerbridge-uk
BACKEND_URL=http://127.0.0.1:8000 frontend/.venv/bin/streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Open:

```text
http://localhost:8501
```

Notes for macOS:

- `docker --version` fails with `zsh: command not found: docker` unless Docker Desktop is installed. You can ignore this for local Python development.
- `date -d` is a Linux command. On macOS, use `date -j -f` for parsing dates, or use normal `date` for the current date/time.
