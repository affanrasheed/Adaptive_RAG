# Running Adaptive RAG with Docker

This document provides instructions for running the Adaptive RAG system using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

## Quick Start with Docker Compose

The easiest way to run the system is with Docker Compose:

1. Make sure you have created a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your API keys.

3. Launch the system with Docker Compose:
   ```bash
   docker-compose up
   ```

4. Access the UI:
   - Streamlit UI: http://localhost:8501
   - Gradio UI: http://localhost:7860
   - Flask UI: http://localhost:5000

## Running without Docker Compose

If you prefer to use Docker directly:

1. Build the Docker image:
   ```bash
   docker build -t adaptive-rag .
   ```

2. Run the container with your preferred UI:
   ```bash
   # For Streamlit UI (default)
   docker run -p 8501:8501 -v "$(pwd)/.env:/app/.env" adaptive-rag
   
   # For Gradio UI
   docker run -p 7860:7860 -v "$(pwd)/.env:/app/.env" adaptive-rag python ui/launch_ui.py --ui gradio
   
   # For Flask UI
   docker run -p 5000:5000 -v "$(pwd)/.env:/app/.env" adaptive-rag python ui/launch_ui.py --ui flask
   ```

## Customizing the Docker Setup

### Changing the Default UI

Edit the `docker-compose.yml` file and modify the `command` line to specify your preferred UI:

```yaml
command: python ui/launch_ui.py --ui [streamlit|gradio|flask]
```

### Persisting Data

To persist the vectorstore data between container restarts, add a volume for the Chroma database:

```yaml
volumes:
  - ./.env:/app/.env
  - ./chroma_db:/app/chroma_db
```

## Troubleshooting

### API Key Issues

If you encounter API key errors, make sure your `.env` file is properly mounted in the container and contains valid API keys.

### Port Conflicts

If you have port conflicts, modify the port mappings in the `docker-compose.yml` file:

```yaml
ports:
  - "8502:8501"  # Maps host port 8502 to container port 8501
```

### Resource Limitations

The system may require significant memory, especially for large vector databases. If you encounter memory issues, increase the container's memory limit:

```yaml
deploy:
  resources:
    limits:
      memory: 4G
```