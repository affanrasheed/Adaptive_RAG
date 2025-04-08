"""Example of streaming the Adaptive RAG workflow execution."""

import sys
import os
from pathlib import Path
from pprint import pprint

# Add the parent directory to the path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.app import AdaptiveRAG
from src.config import Config

def main():
    """Run an example of streaming the Adaptive RAG workflow."""
    # Create configuration
    config = Config(enable_tracing=False)
    
    # Initialize the RAG system
    rag = AdaptiveRAG(config=config, debug=True)
    
    # Example question that should involve query transformation
    question = "Tell me about memory systems in LLM agents"
    print(f"\nQuestion: {question}")
    print("\n=== Streaming Workflow Execution ===")
    
    # Stream workflow execution
    for output in rag.stream_query(question):
        for key, value in output.items():
            # Print node execution
            print(f"Node '{key}':")
            
            # Optional: print state details
            # Uncomment the following to see full state details
            # if "keys" in value:
            #     pprint(value["keys"], indent=2)
            
        print("\n---\n")
    
    # Get the final answer
    final_result = rag.query(question)
    print("\n=== Final Answer ===")
    print(final_result.answer)

if __name__ == "__main__":
    main()