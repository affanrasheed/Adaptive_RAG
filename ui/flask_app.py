"""Flask web application for Adaptive RAG system."""

import os
import sys
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session

# Add the parent directory to the path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.app import AdaptiveRAG
from src.config import Config

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize RAG system
config = Config(enable_tracing=False)
rag = AdaptiveRAG(config=config, debug=False)

@app.route('/')
def index():
    """Render the main page."""
    # Initialize session variables if they don't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    """Process a query and return the response."""
    data = request.json
    query = data.get('query', '')
    show_sources = data.get('show_sources', True)
    show_workflow = data.get('show_workflow', False)
    temperature = float(data.get('temperature', 0.0))
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Capture workflow steps if requested
        workflow_steps = []
        if show_workflow:
            for output in rag.stream_query(query):
                for key, value in output.items():
                    workflow_steps.append(key)
        
        # Get the final result
        result = rag.query(query)
        
        # Format sources if requested
        sources = []
        if show_sources and result.documents:
            for i, doc in enumerate(result.documents):
                source = {
                    'content': doc.page_content,
                    'metadata': {}
                }
                if hasattr(doc, 'metadata'):
                    source['metadata'] = doc.metadata
                sources.append(source)
        
        # Prepare response
        response = {
            'answer': result.answer,
            'sources': sources,
            'workflow': workflow_steps,
            'routing': result.routing_decision
        }
        
        # Update chat history in session
        chat_history = session.get('chat_history', [])
        chat_history.append({
            'user': query,
            'assistant': result.answer
        })
        session['chat_history'] = chat_history
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_document', methods=['POST'])
def add_document():
    """Add a document URL to the RAG system."""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        rag.add_documents(urls=[url])
        return jsonify({'success': f'Added document: {url}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear the chat history."""
    session['chat_history'] = []
    return jsonify({'success': 'Chat history cleared'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create static directory if it doesn't exist
    static_dir = Path(__file__).parent / 'static'
    static_dir.mkdir(exist_ok=True)
    
    app.run(debug=True)