# Adaptive RAG User Guide

This guide provides comprehensive instructions for using the Adaptive RAG system.

## Table of Contents

- [Getting Started](#getting-started)
- [Using the API](#using-the-api)
- [Using the UIs](#using-the-uis)
- [Configuration Options](#configuration-options)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/affanrasheed/Adaptive_RAG.git
   cd Adaptive_RAG
   ```

2. Set up the environment:
   ```bash
   # On Linux/Mac
   ./setup.sh
   
   # On Windows
   setup.bat
   ```

3. Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Quick Start

To quickly test the system:

```bash
# Run a basic example
python examples/simple_question.py

# Launch the UI
python ui/launch_ui.py
```

## Using the API

The system can be used programmatically via its Python API:

```python
from adaptive_rag import AdaptiveRAG
from adaptive_rag import Config

# Create custom configuration (optional)
config = Config(
    document_urls=[
        "https://example.com/document1.html",
        "https://example.com/document2.html",
    ],
    enable_tracing=True
)

# Initialize the system
rag = AdaptiveRAG(config=config)

# Process a query
result = rag.query("What are the types of agent memory?")

# Access results
print(f"Answer: {result.answer}")
print(f"Sources: {len(result.documents)} documents retrieved")
print(f"Routing decision: {result.routing_decision}")

# Stream the processing (to see intermediate steps)
for output in rag.stream_query("What is prompt engineering?"):
    for key, value in output.items():
        print(f"Step: {key}")
```

### Adding Documents

You can add documents to the system:

```python
# Add from URLs
rag.add_documents(urls=["https://example.com/new-document.html"])

# Add from documents
from langchain.schema import Document
docs = [
    Document(page_content="Example content", metadata={"source": "manual"})
]
rag.add_documents(documents=docs)
```

## Using the UIs

The system provides three different UI options:

### Streamlit UI

The Streamlit UI offers a simple, clean interface:

```bash
python ui/launch_ui.py --ui streamlit
```

Features:
- Chat interface for asking questions
- Sources display for viewing retrieved documents
- Settings panel for configuration
- Document addition capability

### Gradio UI

The Gradio UI provides a more polished experience:

```bash
python ui/launch_ui.py --ui gradio
```

Features:
- Advanced chat interface
- Detailed source and workflow visualization
- Real-time workflow streaming
- Configuration options

### Flask UI

The Flask UI offers a traditional web application:

```bash
python ui/launch_ui.py --ui flask
```

Features:
- Responsive design
- Multiple tabs for different information
- Document management
- Advanced configuration

## Configuration Options

The system can be configured through the `Config` class:

### Model Selection

```python
config = Config(
    models={
        "router": "gpt-4o-mini",   # Model for routing queries
        "generator": "gpt-4o",      # Model for generating answers
        "grader": "gpt-4o-mini",    # Model for grading documents/answers
        "rewriter": "gpt-4o-mini",  # Model for query transformation
    }
)
```

### Vectorstore Settings

```python
config = Config(
    vectorstore_settings={
        "collection_name": "my-custom-collection",
        "chunk_size": 1000,         # Size of document chunks
        "chunk_overlap": 100,       # Overlap between chunks
    }
)
```

### Web Search Settings

```python
config = Config(
    web_search_settings={
        "num_results": 5,           # Number of web search results
    }
)
```

## Advanced Usage

### Custom Workflow

You can build custom workflows by extending the system components:

```python
from adaptive_rag.components import VectorStoreRetriever, QueryRouter
from adaptive_rag.workflow import WorkflowNodes, WorkflowEdges, AdaptiveRAGWorkflow

# Create custom components
retriever = VectorStoreRetriever(
    collection_name="custom-collection",
    search_kwargs={"k": 10}
)

# Initialize workflow with custom components
nodes = WorkflowNodes(
    retriever=retriever,
    # Other components...
)

edges = WorkflowEdges(
    # Components...
)

# Create workflow
workflow = AdaptiveRAGWorkflow(
    nodes=nodes,
    edges=edges,
    debug=True,
)

# Use the workflow
result = workflow.run("What are the types of agent memory?")
```

### Using Docker

The system can be run using Docker:

```bash
# Using Docker Compose (recommended)
docker-compose up

# Manually with Docker
docker build -t adaptive-rag .
docker run -p 8501:8501 -v ./.env:/app/.env adaptive-rag
```

For more details, see [DOCKER.md](../DOCKER.md).

## Troubleshooting

### API Key Issues

If you encounter errors related to API keys:

1. Ensure your `.env` file is properly set up
2. Check that the API keys are valid
3. Verify you have necessary permissions/quota for the APIs

### Memory Usage

The system may require significant memory, especially for large vector databases:

1. Reduce the number of documents in the vectorstore
2. Decrease chunk size in the configuration
3. Use smaller models for components that don't need the largest models

### Slow Performance

If the system is running slowly:

1. Use smaller models for less critical components
2. Reduce the number of documents retrieved
3. Decrease complexity of the workflow by disabling certain components

### Web Search Not Working

If web search functionality isn't working:

1. Verify your Tavily API key is valid
2. Check your internet connection
3. Ensure you haven't exceeded API request limits