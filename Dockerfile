# Multi-stage Dockerfile for Food Recognition & Calorie Tracker
# Stage 1: Build & setup dependency wheels
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime system dependencies for OpenCV and SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Create necessary directories and set correct ownership
RUN mkdir -p data models uploads output

# Copy source code and files
COPY src/ ./src/
COPY ui/ ./ui/
COPY config.py .
COPY README.md .

# Expose ports: 8501 for Streamlit, 5000 for Flask API
EXPOSE 8501
EXPOSE 5000

# Streamlit-specific production environment settings
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# By default, run the Streamlit interface
CMD ["streamlit", "run", "ui/app.py"]
