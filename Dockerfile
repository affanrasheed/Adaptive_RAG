FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY ui/requirements.txt ./ui/
COPY ui/gradio_requirements.txt ./ui/
COPY ui/flask_requirements.txt ./ui/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r ui/requirements.txt \
    && pip install --no-cache-dir -r ui/gradio_requirements.txt \
    && pip install --no-cache-dir -r ui/flask_requirements.txt

# Copy source code
COPY . .

# Install the package
RUN pip install -e .

# Create a .env file from the example if needed
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to run
CMD ["python", "ui/launch_ui.py", "--ui", "streamlit"]

# Expose ports for the different UIs
EXPOSE 8501 7860 5000