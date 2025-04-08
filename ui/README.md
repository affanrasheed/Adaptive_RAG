# Adaptive RAG UI

This directory contains multiple user interface options for the Adaptive RAG system.

## Available UIs

1. **Streamlit UI** - A simple, interactive web interface built with Streamlit
2. **Gradio UI** - A more polished UI with advanced features built with Gradio
3. **Flask UI** - A traditional web application built with Flask

## Getting Started

The easiest way to launch any of the UIs is by using the launcher script:

```bash
python launch_ui.py --ui [streamlit|gradio|flask]
```

This launcher will automatically install any required dependencies for the selected UI.

## UI Features

All UIs provide the following core features:
- Chat interface for interacting with the Adaptive RAG system
- Display of sources used in generating responses
- Configuration options (temperature, etc.)
- Option to view workflow execution steps

### Streamlit UI

![Streamlit UI](../screenshots/streamlit_ui.png)

The Streamlit UI provides a simple, clean interface that focuses on ease of use. It's great for quick interactions and demonstrations.

To launch manually:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Gradio UI

![Gradio UI](../screenshots/gradio_ui.png)

The Gradio UI offers a more polished look with advanced features like tabs for different information displays and a more sophisticated chat interface.

To launch manually:
```bash
pip install -r gradio_requirements.txt
python gradio_app.py
```

### Flask UI

![Flask UI](../screenshots/flask_ui.png)

The Flask UI provides a traditional web application experience with a clean, responsive design.

To launch manually:
```bash
pip install -r flask_requirements.txt
python flask_app.py
```

## Adding Custom UIs

You can create your own UI by implementing a new interface that connects to the Adaptive RAG system. See the existing implementations for examples of how to integrate with the system.

