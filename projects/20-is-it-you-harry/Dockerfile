FROM python:3.10-slim

LABEL maintainer="workshop-poudlard-epsi"
LABEL description="CNN Character Recognition - IS IT YOU HARRY?"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY data/ ./data/
COPY models/ ./models/

# Expose Jupyter port
EXPOSE 8888

# Create necessary directories
RUN mkdir -p /app/models /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command: launch Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
