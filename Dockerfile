# =============================================================================
# Tokoku Assistant — Dockerfile
# =============================================================================
# Base image: Python 3.12 slim (minimal footprint)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# --- System dependencies ---
# curl is needed by the healthcheck in docker-compose
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- Python dependencies (separate layer for caching) ---
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

# --- Application source ---
# Only copy what the app needs at runtime
COPY app/          ./app/
COPY src/          ./src/
COPY config/       ./config/
COPY .streamlit/   ./.streamlit/

# --- Environment ---
# Ensure Python finds src.* modules
ENV PYTHONPATH=/app
# Prevent buffered output (important for Streamlit logs in Docker)
ENV PYTHONUNBUFFERED=1
# Force UTF-8 for stdout/stderr (Windows compat fix carries over gracefully)
ENV PYTHONIOENCODING=utf-8

# --- Port ---
EXPOSE 8501

# --- Entrypoint ---
CMD ["streamlit", "run", "app/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
