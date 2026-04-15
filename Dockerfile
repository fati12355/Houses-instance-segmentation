FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (with retry and non-interactive)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/
COPY app.py .
# COPY models/ ./models/

EXPOSE 5000

CMD ["python", "app.py"]