"""Retrieval components for Adaptive RAG."""

from typing import List, Dict, Any, Optional
from langchain.schema import Document, BaseRetriever
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorStoreRetriever:
    """Component for retrieving documents from a vector store."""
    
    def __init__(
        self, 
        vectorstore: Optional[Chroma] = None,
        collection_name: str = "adaptive-rag-collection",
        embedding_model: Optional[str] = None,
        search_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the retriever.
        
        Args:
            vectorstore: Optional pre-built vectorstore
            collection_name: Collection name for persistence
            embedding_model: Optional specific OpenAI embedding model
            search_kwargs: Additional search parameters
        """
        self.collection_name = collection_name
        self.search_kwargs = search_kwargs or {"k": 4}
        
        # Set up embeddings
        embedding_kwargs = {}
        if embedding_model:
            embedding_kwargs["model"] = embedding_model
            
        self.embeddings = OpenAIEmbeddings(**embedding_kwargs)
        
        # Use provided vectorstore or try to load from persistence
        if vectorstore:
            self.vectorstore = vectorstore
        else:
            try:
                self.vectorstore = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                )
            except Exception as e:
                print(f"Could not load existing vectorstore: {e}")
                # Initialize empty vectorstore
                self.vectorstore = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                )
                
        # Create retriever from vectorstore
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs=self.search_kwargs
        )
        
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve documents for a query.
        
        Args:
            query: Query to retrieve documents for
            
        Returns:
            List of retrieved documents
        """
        return self.retriever.invoke(query)
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vectorstore.
        
        Args:
            documents: Documents to add
        """
        self.vectorstore.add_documents(documents)

class HybridRetriever:
    """Combines multiple retrievers with configurable weights."""
    
    def __init__(
        self,
        retrievers: List[BaseRetriever],
        weights: Optional[List[float]] = None,
    ):
        """
        Initialize hybrid retriever.
        
        Args:
            retrievers: List of retrievers to combine
            weights: Optional weights for each retriever (must match length of retrievers)
        """
        self.retrievers = retrievers
        
        # Default to equal weights if not provided
        if weights:
            if len(weights) != len(retrievers):
                raise ValueError("Number of weights must match number of retrievers")
            self.weights = weights
        else:
            self.weights = [1.0] * len(retrievers)
            
    def retrieve(self, query: str, limit: int = 4) -> List[Document]:
        """
        Retrieve documents from all retrievers.
        
        Args:
            query: Query to retrieve documents for
            limit: Maximum number of documents to return
            
        Returns:
            Combined list of documents
        """
        all_docs = []
        
        # Get documents from each retriever
        for retriever, weight in zip(self.retrievers, self.weights):
            docs = retriever.invoke(query)
            
            # Add weight to document scores (if available)
            for doc in docs:
                if hasattr(doc, "metadata") and "score" in doc.metadata:
                    doc.metadata["score"] *= weight
                # Ensure each doc has a retriever source
                if hasattr(doc, "metadata"):
                    doc.metadata["retriever"] = retriever.__class__.__name__
                
            all_docs.extend(docs)
            
        # Sort by score if available
        try:
            all_docs = sorted(
                all_docs, 
                key=lambda x: x.metadata.get("score", 0), 
                reverse=True
            )
        except:
            # If sorting fails, just return the combined docs
            pass
            
        # Limit the number of results
        return all_docs[:limit]