
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install Node.js, npm, and Java for XAI integrations
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nodejs npm default-jre-headless ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy CareerBridge backend
COPY . .

# Install Meterless TypeScript runner
RUN npm ci --include=dev \
    --prefix /app/app/xai/integrations/meterless

EXPOSE 8000

# Start FastAPI using the port supplied by Render
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
