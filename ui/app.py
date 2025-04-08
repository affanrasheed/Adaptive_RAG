"""Streamlit UI for Adaptive RAG system."""

import os
import sys
import streamlit as st
from pathlib import Path
import time

# Add the parent directory to the path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.app import AdaptiveRAG
from src.config import Config

# Page config
st.set_page_config(
    page_title="Adaptive RAG System",
    page_icon="🧠",
    layout="wide",
)

# Initialize session state
if "rag" not in st.session_state:
    with st.spinner("Initializing Adaptive RAG system..."):
        # Create configuration
        config = Config(enable_tracing=False)
        
        # Initialize the RAG system
        st.session_state.rag = AdaptiveRAG(config=config, debug=False)
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "loading" not in st.session_state:
    st.session_state.loading = False
    
# UI Components
st.title("🧠 Adaptive RAG System")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This is an Adaptive RAG (Retrieval Augmented Generation) system that:
    
    - Intelligently routes queries between vector database and web search
    - Filters irrelevant documents
    - Transforms queries when necessary
    - Detects hallucinations in answers
    - Ensures answers address the original question
    """)
    
    st.header("Configuration")
    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    show_sources = st.checkbox("Show sources", value=True)
    show_workflow = st.checkbox("Show workflow steps", value=False)
    
    st.header("Document Sources")
    st.markdown("""
    The system has been loaded with documents about:
    - Agent architectures
    - Prompt engineering
    - Adversarial attacks on LLMs
    """)
    
    # Optional: Add form to add more document URLs
    with st.expander("Add Documents"):
        with st.form("add_docs_form"):
            doc_url = st.text_input("Document URL")
            submitted = st.form_submit_button("Add Document")
            if submitted and doc_url:
                with st.spinner("Adding document..."):
                    try:
                        st.session_state.rag.add_documents(urls=[doc_url])
                        st.success(f"Added document: {doc_url}")
                    except Exception as e:
                        st.error(f"Error adding document: {e}")

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if enabled and available
            if show_sources and message["role"] == "assistant" and "sources" in message:
                with st.expander("Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.markdown(f"**Source {i+1}:**")
                        if "url" in source:
                            st.markdown(f"[{source.get('title', 'Link')}]({source['url']})")
                        st.markdown(f"```\n{source['content'][:300]}...\n```")
            
            # Show workflow if enabled and available
            if show_workflow and message["role"] == "assistant" and "workflow" in message:
                with st.expander("Workflow Steps"):
                    for step in message["workflow"]:
                        st.markdown(f"**{step['node']}**")
                        if "details" in step:
                            st.markdown(f"{step['details']}")

# Input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Set loading state
    st.session_state.loading = True
    
    # Display assistant response with a spinner
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Thinking...")
        
        workflow_steps = []
        
        try:
            # Process the query and capture workflow steps if enabled
            if show_workflow:
                workflow_container = st.empty()
                workflow_container.markdown("Processing query through workflow...")
                
                # Stream workflow
                for output in st.session_state.rag.stream_query(user_input):
                    for key, value in output.items():
                        workflow_steps.append({
                            "node": key,
                            "details": f"Processing step: {key}"
                        })
                        workflow_text = "\n\n".join([f"**{step['node']}**" for step in workflow_steps])
                        workflow_container.markdown(f"**Workflow Steps:**\n{workflow_text}")
                        time.sleep(0.5)  # Slow down a bit for UI effect
                
                # Clear workflow container
                workflow_container.empty()
            
            # Get final result
            result = st.session_state.rag.query(user_input)
            
            # Update response
            response_placeholder.markdown(result.answer)
            
            # Add to chat history
            sources = []
            for doc in result.documents:
                source = {
                    "content": doc.page_content,
                }
                if hasattr(doc, "metadata"):
                    if "source" in doc.metadata:
                        source["url"] = doc.metadata["source"]
                    if "title" in doc.metadata:
                        source["title"] = doc.metadata["title"]
                sources.append(source)
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": result.answer,
                "sources": sources,
                "workflow": workflow_steps
            })
            
        except Exception as e:
            response_placeholder.markdown(f"Error: {str(e)}")
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f"I encountered an error: {str(e)}"
            })
        
        # Reset loading state
        st.session_state.loading = False