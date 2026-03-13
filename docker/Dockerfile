FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY src/ src/
COPY commands/ commands/
COPY skills/ skills/
COPY tools/ tools/

# Coach-specific data mounted as volume
VOLUME /app/coaches

# FastAPI server
EXPOSE 8000

CMD ["uvicorn", "src.ccp.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
