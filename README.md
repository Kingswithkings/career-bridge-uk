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

For Zoho Mail on Render Free, use the HTTPS API transport (.com region).
Set these in the backend environment:

```text
ZOHO_CLIENT_ID=<Zoho Self Client ID>
ZOHO_CLIENT_SECRET=<Zoho Self Client secret>
ZOHO_FROM_EMAIL=kings@1st-kings.com
ZOHO_REFRESH_TOKEN=<refresh token from the setup helper>
ZOHO_ACCOUNT_ID=<account ID from the setup helper>
```

Run `python3 backend/scripts/setup_zoho_mail.py` in your local terminal. It prompts
for credentials with hidden input, exchanges a fresh Self Client authorization
code using `ZohoMail.messages.CREATE,ZohoMail.accounts.READ`, and finds the sender's
account ID. It saves the refresh token and account ID in a private temporary file
outside the repository. Copy those values into Render, then delete the file.
Never commit or share tokens or client secrets. The helper does not send emails.

When `ZOHO_CLIENT_ID` is set, both welcome and password reset messages use Zoho
over HTTPS. All five values above are required. Access tokens are cached and
refreshed automatically on expiry. Failed sends are logged without provider
response bodies and are not automatically retried. Deploy the updated backend
after saving the settings; saving environment variables alone does not install
this transport. The sender's display name comes from the Zoho mailbox settings.

Alternatively, SMTP welcome email settings in `backend/.env` (also set these in the deployed backend's environment; Render Free blocks SMTP ports):

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

If neither provider is configured, account registration still succeeds and the confirmation
email is skipped.

After successful registration, the backend sends a welcome email to the registered
email address in a background task. The greeting uses the first word of the
registered full name (for example, "Hi Sarah," for "Sarah Jones"), or "Hi there,"
when no name is supplied. Email delivery failures are logged without blocking
registration. Delivery requires a configured email provider; background tasks do not
automatically retry failed sends.

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
