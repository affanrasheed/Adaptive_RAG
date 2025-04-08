"""Main application for Adaptive RAG."""

from typing import List, Dict, Any, Optional
import logging

from .utils.env_setup import setup_required_env_vars
from .config import Config
from .utils.document_loader import load_and_index_urls
from .components.retrievers import VectorStoreRetriever
from .components.searchers import WebSearcher
from .components.generators import RAGGenerator
from .components.transformers import QueryTransformer
from .components.graders import DocumentGrader, HallucinationGrader, AnswerGrader
from .components.routers import QueryRouter
from .workflow.nodes import WorkflowNodes
from .workflow.edges import WorkflowEdges
from .workflow.graph import AdaptiveRAGWorkflow
from .models.data_models import RAGResult

class AdaptiveRAG:
    """Main class for the Adaptive RAG system."""
    
    def __init__(
        self,
        config: Optional[Config] = None,
        debug: bool = False,
    ):
        """
        Initialize the Adaptive RAG system.
        
        Args:
            config: Optional configuration
            debug: Whether to enable debug logging
        """
        # Set up environment
        setup_required_env_vars()
        
        # Create or use config
        self.config = config or Config()
        
        # Set up logging
        if debug:
            logging.basicConfig(level=logging.INFO)
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all components of the system."""
        # Create vectorstore
        try:
            vectorstore = load_and_index_urls(
                urls=self.config.document_urls,
                collection_name=self.config.vectorstore_settings["collection_name"],
                chunk_size=self.config.vectorstore_settings["chunk_size"],
                chunk_overlap=self.config.vectorstore_settings["chunk_overlap"],
            )
        except Exception as e:
            logging.error(f"Error creating vectorstore: {e}")
            vectorstore = None
        
        # Initialize components
        self.retriever = VectorStoreRetriever(
            vectorstore=vectorstore,
            collection_name=self.config.vectorstore_settings["collection_name"],
        )
        
        self.web_searcher = WebSearcher(
            num_results=self.config.web_search_settings["num_results"],
        )
        
        self.generator = RAGGenerator(
            model_name=self.config.models["generator"],
        )
        
        self.query_transformer = QueryTransformer(
            model_name=self.config.models["rewriter"],
        )
        
        self.document_grader = DocumentGrader(
            model_name=self.config.models["grader"],
        )
        
        self.hallucination_grader = HallucinationGrader(
            model_name=self.config.models["grader"],
        )
        
        self.answer_grader = AnswerGrader(
            model_name=self.config.models["grader"],
        )
        
        self.query_router = QueryRouter(
            model_name=self.config.models["router"],
        )
        
        # Create workflow nodes and edges
        self.nodes = WorkflowNodes(
            retriever=self.retriever,
            web_searcher=self.web_searcher,
            generator=self.generator,
            query_transformer=self.query_transformer,
            document_grader=self.document_grader,
            hallucination_grader=self.hallucination_grader,
            answer_grader=self.answer_grader,
        )
        
        self.edges = WorkflowEdges(
            query_router=self.query_router,
            hallucination_grader=self.hallucination_grader,
            answer_grader=self.answer_grader,
        )
        
        # Create workflow
        self.workflow = AdaptiveRAGWorkflow(
            nodes=self.nodes,
            edges=self.edges,
            debug=True,
        )
    
    def query(self, question: str) -> RAGResult:
        """
        Process a query through the RAG system.
        
        Args:
            question: User question
            
        Returns:
            RAG result with answer and metadata
        """
        # Run the workflow
        final_state = self.workflow.run(question)
        
        # Extract results
        answer = final_state.get("generation", "No answer generated")
        documents = final_state.get("documents", [])
        
        # Create result object
        result = RAGResult(
            question=question,
            answer=answer,
            documents=documents,
            routing_decision="vectorstore" if isinstance(documents[0].metadata.get("retriever"), str) and "vector" in documents[0].metadata.get("retriever", "").lower() else "web_search",
            metadata={
                "final_question": final_state.get("question"),
                "original_question": question,
            }
        )
        
        return result
    
    def stream_query(self, question: str):
        """
        Stream the processing of a query through the RAG system.
        
        Args:
            question: User question
            
        Yields:
            Intermediate states of the workflow
        """
        return self.workflow.stream(question)
    
    def add_documents(self, documents=None, urls=None):
        """
        Add documents to the vectorstore.
        
        Args:
            documents: List of documents to add
            urls: List of URLs to load and add
        """
        if urls:
            from .utils.document_loader import load_documents_from_urls, split_documents
            documents = load_documents_from_urls(urls)
            documents = split_documents(
                documents,
                chunk_size=self.config.vectorstore_settings["chunk_size"],
                chunk_overlap=self.config.vectorstore_settings["chunk_overlap"],
            )
        
        if documents:
            self.retriever.add_documents(documents)