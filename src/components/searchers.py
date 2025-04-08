"""Web search components for Adaptive RAG."""

from typing import List, Dict, Any, Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document

class WebSearcher:
    """Component for web search."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        num_results: int = 3,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ):
        """
        Initialize web searcher.
        
        Args:
            api_key: Tavily API key (if not set in environment)
            num_results: Number of results to return
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
        """
        search_args = {"k": num_results}
        
        # Add domain filters if provided
        if include_domains:
            search_args["include_domains"] = include_domains
        if exclude_domains:
            search_args["exclude_domains"] = exclude_domains
            
        # Create the search tool
        tavily_args = {}
        if api_key:
            tavily_args["api_key"] = api_key
            
        self.search_tool = TavilySearchResults(**tavily_args, **search_args)
        
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform web search for a query.
        
        Args:
            query: Query to search for
            
        Returns:
            List of search results
        """
        return self.search_tool.invoke({"query": query})
    
    def search_to_documents(self, query: str) -> List[Document]:
        """
        Perform web search and convert results to documents.
        
        Args:
            query: Query to search for
            
        Returns:
            List of documents from search results
        """
        results = self.search(query)
        
        
        documents = []
        for result in results:
            # Create document from search result
            doc = Document(
                page_content=result["content"],
                metadata={
                    "source": result.get("url", "web-search"),
                    "title": result.get("title", ""),
                    "score": 1.0,  # Default score
                    "retriever": "web_search"
                }
            )
            documents.append(doc)
        return documents