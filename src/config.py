"""Configuration for the Adaptive RAG system."""

import os
from typing import List, Dict, Any, Optional

# Default model configurations
DEFAULT_MODELS = {
    "router": "gpt-4o-mini",
    "generator": "gpt-4o-mini", 
    "grader": "gpt-4o-mini",
    "rewriter": "gpt-4o-mini",
}

# Default vectorstore settings
DEFAULT_VECTORSTORE_SETTINGS = {
    "collection_name": "adaptive-rag-collection",
    "chunk_size": 500,
    "chunk_overlap": 0,
}

# Default web search settings
DEFAULT_WEB_SEARCH_SETTINGS = {
    "num_results": 3,
}

# Default document sources for indexing
DEFAULT_DOCUMENT_URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

class Config:
    """Configuration class for Adaptive RAG."""
    
    def __init__(
        self,
        models: Optional[Dict[str, str]] = None,
        vectorstore_settings: Optional[Dict[str, Any]] = None,
        web_search_settings: Optional[Dict[str, Any]] = None,
        document_urls: Optional[List[str]] = None,
        enable_tracing: bool = False,
    ):
        """
        Initialize configuration.
        
        Args:
            models: Model configuration for different components
            vectorstore_settings: Settings for the vectorstore
            web_search_settings: Settings for web search
            document_urls: URLs to index in the vectorstore
            enable_tracing: Whether to enable LangSmith tracing
        """
        self.models = models or DEFAULT_MODELS.copy()
        self.vectorstore_settings = vectorstore_settings or DEFAULT_VECTORSTORE_SETTINGS.copy()
        self.web_search_settings = web_search_settings or DEFAULT_WEB_SEARCH_SETTINGS.copy()
        self.document_urls = document_urls or DEFAULT_DOCUMENT_URLS.copy()
        
        # Set up tracing
        self.enable_tracing = enable_tracing
        if enable_tracing:
            os.environ["LANGSMITH_TRACING"] = "true"
            # Ensure project name is set
            if not os.environ.get("LANGSMITH_PROJECT"):
                os.environ["LANGSMITH_PROJECT"] = "Adaptive_RAG"