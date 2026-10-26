
FROM python:3.11-slim-bookworm

# Keep the backend package structure intact
WORKDIR /workspace

# Install Node.js, npm, and Java
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nodejs npm default-jre-headless ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /workspace/backend/requirements.txt

RUN pip install --no-cache-dir \
    -r /workspace/backend/requirements.txt

# Copy the backend source code
COPY . /workspace/backend/

# Install Meterless TypeScript runner
RUN npm ci --include=dev \
    --prefix /workspace/backend/app/xai/integrations/meterless

# Make backend.app importable
ENV PYTHONPATH=/workspace

EXPOSE 8000

# Start FastAPI
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
