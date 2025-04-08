"""Gradio UI for Adaptive RAG system."""

import os
import sys
import json
from pathlib import Path
import gradio as gr
import time

# Add the parent directory to the path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.app import AdaptiveRAG
from src.config import Config
from src.models.data_models import RAGResult

# Initialize RAG system
config = Config(enable_tracing=False)
rag = AdaptiveRAG(config=config, debug=False)

# Theme and styling
theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
).set(
    body_text_color="#303030",
    block_label_text_size="15px",
    button_primary_background_fill="*primary_500",
    button_primary_text_color="white",
)

# Custom CSS
custom_css = """
.gradio-container {
    max-width: 1200px !important;
}
.sources-accordion .accordion-content {
    max-height: 300px;
    overflow-y: auto;
}
.workflow-box {
    border-left: 3px solid #4a69bd;
    padding-left: 10px;
    margin: 10px 0;
    background-color: #f5f7ff;
}
.document-box {
    border: 1px solid #ddd;
    padding: 10px;
    margin: 5px 0;
    border-radius: 5px;
}
.header-box {
    text-align: center;
    margin-bottom: 20px;
}
"""

# Initialize conversation memory
conversation_history = []
workflow_steps = []

def add_document(url):
    """Add a document URL to the RAG system."""
    if not url or not url.strip():
        return "Please enter a valid URL"
    
    try:
        rag.add_documents(urls=[url])
        return f"Successfully added document: {url}"
    except Exception as e:
        return f"Error adding document: {str(e)}"

def process_query(message, history, show_sources, show_workflow, temperature):
    """Process a query and return the response with optional sources and workflow."""
    global workflow_steps
    workflow_steps = []
    
    # Set temperature
    rag.generator.llm.temperature = float(temperature)
    
    # Initialize response
    response = ""
    
    # Stream workflow steps if requested
    if show_workflow:
        response = "Processing your query...\n\n"
        yield response
        
        for output in rag.stream_query(message):
            for key, value in output.items():
                step = f"Step: {key}"
                workflow_steps.append(step)
                
                # Update response with workflow steps
                response = "Processing your query...\n\n"
                response += "\n".join(f"- {s}" for s in workflow_steps)
                yield response
                time.sleep(0.3)  # Slight delay for better UX
    
    # Get final result
    result = rag.query(message)
    
    # Format final response
    response = result.answer
    
    # Add sources if requested
    if show_sources and result.documents:
        sources_text = "\n\nSources:\n"
        for i, doc in enumerate(result.documents):
            source_info = f"\n[{i+1}] "
            if hasattr(doc, "metadata") and "source" in doc.metadata:
                source_info += f"From: {doc.metadata['source']}\n"
            source_info += f"Content: {doc.page_content[:150]}...\n"
            sources_text += source_info
        
        # Don't include sources in the chatbot, we'll display them separately
        sources_display = sources_text
    else:
        sources_display = ""
    
    # Final response without sources
    yield response
    
    # Return additional data through conversation memory
    conversation_history.append({
        "query": message,
        "response": response,
        "sources": [{"content": doc.page_content, "metadata": doc.metadata} for doc in result.documents] if result.documents else [],
        "workflow": workflow_steps.copy(),
        "routing": result.routing_decision
    })

def display_conversation_details():
    """Display the details of the most recent conversation."""
    if not conversation_history:
        return "No conversation history yet", "No sources available", "No workflow information"
    
    last_conv = conversation_history[-1]
    
    # Format sources
    sources_html = ""
    for i, source in enumerate(last_conv["sources"]):
        sources_html += f"<div class='document-box'><strong>Source {i+1}:</strong><br>"
        if "metadata" in source and "source" in source["metadata"]:
            sources_html += f"<strong>From:</strong> {source['metadata']['source']}<br>"
        sources_html += f"<strong>Content:</strong> {source['content'][:300]}...<br></div>"
    
    if not sources_html:
        sources_html = "No sources available for this response"
    
    # Format workflow
    workflow_html = ""
    for step in last_conv["workflow"]:
        workflow_html += f"<div class='workflow-box'>{step}</div>"
    
    if not workflow_html:
        workflow_html = "No workflow information available"
    
    # Format query info
    query_info = f"<strong>Query:</strong> {last_conv['query']}<br>"
    query_info += f"<strong>Routing decision:</strong> {last_conv.get('routing', 'Unknown')}<br>"
    
    return query_info, sources_html, workflow_html

def clear_history():
    """Clear the conversation history."""
    global conversation_history, workflow_steps
    conversation_history = []
    workflow_steps = []
    return [], None, "", ""

# Create the Gradio app
with gr.Blocks(theme=theme, css=custom_css) as demo:
    with gr.Row():
        with gr.Column():
            gr.HTML("<div class='header-box'><h1>🧠 Adaptive RAG System</h1><p>An intelligent retrieval augmented generation system that adapts to your queries</p></div>")
    
    with gr.Row():
        with gr.Column(scale=7):
            # Chat interface
            chatbot = gr.Chatbot(
                height=500,
                bubble_full_width=False,
                show_label=False,
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask me anything...",
                    scale=9,
                    container=False,
                    show_label=False,
                )
                submit = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                clear = gr.Button("Clear Conversation")
        
        with gr.Column(scale=3):
            with gr.Tab("Settings"):
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.1,
                    value=0.0,
                    label="Temperature",
                )
                show_sources = gr.Checkbox(
                    value=True,
                    label="Show sources",
                )
                show_workflow = gr.Checkbox(
                    value=False,
                    label="Show workflow steps",
                )
                
                with gr.Accordion("Add Document", open=False):
                    doc_url = gr.Textbox(
                        placeholder="Enter document URL",
                        label="Document URL",
                    )
                    add_doc_btn = gr.Button("Add Document")
                    add_doc_result = gr.Textbox(label="Result")
            
            with gr.Tab("Conversation Details"):
                query_info = gr.HTML(label="Query Info")
                sources = gr.HTML(label="Sources")
                workflow = gr.HTML(label="Workflow")
    
    # Set up interactions
    submit_click = submit.click(
        process_query,
        inputs=[msg, chatbot, show_sources, show_workflow, temperature],
        outputs=[chatbot],
    )
    
    submit_click.then(
        display_conversation_details,
        inputs=[],
        outputs=[query_info, sources, workflow],
    )
    
    msg.submit(
        process_query,
        inputs=[msg, chatbot, show_sources, show_workflow, temperature],
        outputs=[chatbot],
    ).then(
        display_conversation_details,
        inputs=[],
        outputs=[query_info, sources, workflow],
    )
    
    clear.click(
        clear_history,
        inputs=[],
        outputs=[chatbot, msg, query_info, sources, workflow],
    )
    
    add_doc_btn.click(
        add_document,
        inputs=[doc_url],
        outputs=[add_doc_result],
    )
    
    # Description in the footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 20px;">
        <p><strong>About this system:</strong> This Adaptive RAG system intelligently routes queries between vector database and web search, 
        filters irrelevant documents, transforms queries when necessary, and ensures high-quality responses.</p>
    </div>
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()