# Build Stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Runtime Stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r cbcs && useradd -r -g cbcs cbcs

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY backend /app/backend
COPY .env /app/.env

# Create directories for logs/artifacts with permissions
RUN mkdir -p /app/artifacts /app/logs && \
    chown -R cbcs:cbcs /app

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER cbcs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Default command (overridden by docker-compose for specific ports)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
