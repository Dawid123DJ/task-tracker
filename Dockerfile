FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5) or exit(1)"

# Expose port and run application
EXPOSE 8000
CMD ["python", "task_tracker.py"]