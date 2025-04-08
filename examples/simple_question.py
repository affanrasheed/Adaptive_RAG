"""Example of using the Adaptive RAG system for a simple question."""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.app import AdaptiveRAG
from src.config import Config

def main():
    """Run a simple example of the Adaptive RAG system."""
    # Create configuration
    config = Config(
        # Customize default URLs
        document_urls=[
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ],
        # Enable tracing if needed
        enable_tracing=False,
    )
    
    # Initialize the RAG system
    rag = AdaptiveRAG(config=config, debug=True)
    

    # Example question that should use web search
    question = "What player at the Bears expected to draft first in the 2024 NFL draft?"
    print(f"\nQuestion: {question}")
    
    # Get answer
    print("\nProcessing...")
    result = rag.query(question)
    
    # Print results
    print("\n=== Results ===")
    print(f"Routing decision: {result.routing_decision}")
    print(f"\nAnswer: {result.answer}")
    print("\nSources:")
    for i, doc in enumerate(result.documents):
        print(f"\n  Document {i+1}:")
        metadata = doc.metadata
        if "source" in metadata:
            print(f"    Source: {metadata['source']}")
        print(f"    Content: {doc.page_content[:100]}...")

    # Example question that should use vectorstore
    question = "What are the types of agent memory?"
    print(f"\nQuestion: {question}")
    
    # Get answer
    print("\nProcessing...")
    result = rag.query(question)
    
    # Print results
    print("\n=== Results ===")
    print(f"Routing decision: {result.routing_decision}")
    print(f"\nAnswer: {result.answer}")
    print("\nSources:")
    for i, doc in enumerate(result.documents):
        print(f"\n  Document {i+1}:")
        metadata = doc.metadata
        if "source" in metadata:
            print(f"    Source: {metadata['source']}")
        print(f"    Content: {doc.page_content[:100]}...")

    

if __name__ == "__main__":
    main()