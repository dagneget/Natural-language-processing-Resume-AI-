# Use Python 3.11-slim for stability (Avoids Py3.14 Windows DLL issues)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-multipart

# Pre-download ML models to avoid latency on first run
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python -c "from gliner import GLiNER; GLiNER.from_pretrained('urchade/gliner_small-v2.1')"

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]