"""Environment setup utilities for Adaptive RAG."""

import os
import getpass
from typing import Optional
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    
def set_env_var(var_name: str, prompt: Optional[str] = None):
    """
    Set environment variable if not already set.
    
    Args:
        var_name: Name of the environment variable
        prompt: Optional prompt to display when requesting input
    """
    if not os.environ.get(var_name):
        prompt_text = prompt if prompt else f"{var_name}: "
        os.environ[var_name] = getpass.getpass(prompt_text)

def setup_required_env_vars():
    """Set up all required environment variables."""
    # Load from .env file first
    load_environment()
    
    # Required API keys
    set_env_var("OPENAI_API_KEY")
    set_env_var("TAVILY_API_KEY")
    
    # Optional: LangSmith for tracing
    if os.environ.get("ENABLE_LANGSMITH", "false").lower() == "true":
        os.environ["LANGSMITH_TRACING"] = "true"
        set_env_var("LANGSMITH_API_KEY")
        
        # Set default LangSmith project if not specified
        if not os.environ.get("LANGSMITH_PROJECT"):
            os.environ["LANGSMITH_PROJECT"] = "Adaptive_RAG"