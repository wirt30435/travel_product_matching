# Minimal Dockerfile for Cloud Run (linux/amd64)
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Copy and install requirements in one layer
COPY requirements-gcp.txt .
RUN pip install --no-cache-dir -r requirements-gcp.txt

# Copy app files
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Start command
CMD streamlit run main_gcp.py --server.port=$PORT --server.address=0.0.0.0
