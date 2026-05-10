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

For deployment, set `DATABASE_URL` to a persistent PostgreSQL database. The
default SQLite database is only suitable for local development; on ephemeral
hosts such as Render, accounts can disappear after a restart or redeploy, which
will make valid-looking logins return `401 Invalid email or password`.

Optional registration confirmation email settings in `backend/.env`:

```text
DATABASE_URL=postgresql://user:password@host:5432/database
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp-user
SMTP_PASSWORD=your-smtp-password
SMTP_FROM_EMAIL=no-reply@example.com
SMTP_FROM_NAME=CareerBridge UK
SMTP_USE_TLS=true
FRONTEND_URL=https://your-frontend-url
```

If these are not set, account registration still succeeds and the confirmation
email is skipped.

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
