"""Workflow nodes for Adaptive RAG."""

from typing import Dict, Any, List
from ..models.data_models import GraphState
from ..components.retrievers import VectorStoreRetriever
from ..components.searchers import WebSearcher
from ..components.generators import RAGGenerator
from ..components.transformers import QueryTransformer
from ..components.graders import DocumentGrader, HallucinationGrader, AnswerGrader
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

class WorkflowNodes:
    """Contains all the node functions for the workflow graph."""
    
    def __init__(
        self,
        retriever: VectorStoreRetriever,
        web_searcher: WebSearcher,
        generator: RAGGenerator,
        query_transformer: QueryTransformer,
        document_grader: DocumentGrader,
        hallucination_grader: HallucinationGrader,
        answer_grader: AnswerGrader,
    ):
        """
        Initialize workflow nodes.
        
        Args:
            retriever: Vectorstore retriever component
            web_searcher: Web search component
            generator: RAG generator component
            query_transformer: Query transformation component
            document_grader: Document grading component
            hallucination_grader: Hallucination grading component
            answer_grader: Answer grading component
        """
        self.retriever = retriever
        self.web_searcher = web_searcher
        self.generator = generator
        self.query_transformer = query_transformer
        self.document_grader = document_grader
        self.hallucination_grader = hallucination_grader
        self.answer_grader = answer_grader
    
    def retrieve(self, state: GraphState) -> Dict[str, Any]:
        """
        Retrieve documents from vectorstore.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with retrieved documents
        """
        logger.info("Node: RETRIEVE")
        question = state["question"]
        
        # Retrieve documents
        documents = self.retriever.retrieve(question)
        
        return {"documents": documents, "question": question}
    
    def web_search(self, state: GraphState) -> Dict[str, Any]:
        """
        Perform web search.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with web search results
        """
        logger.info("Node: WEB SEARCH")
        question = state["question"]
        
        # Perform web search
        documents = self.web_searcher.search_to_documents(question)
        
        return {"documents": documents, "question": question}
    
    def grade_documents(self, state: GraphState) -> Dict[str, Any]:
        """
        Grade retrieved documents for relevance.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with filtered documents
        """
        logger.info("Node: GRADE DOCUMENTS")
        question = state["question"]
        documents = state["documents"]
        
        # Grade and filter documents
        filtered_docs = self.document_grader.filter_documents(documents, question)
        
        return {"documents": filtered_docs, "question": question}
    
    def transform_query(self, state: GraphState) -> Dict[str, Any]:
        """
        Transform query to improve retrieval.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with transformed query
        """
        logger.info("Node: TRANSFORM QUERY")
        question = state["question"]
        documents = state.get("documents", [])
        
        # Transform query
        better_question = self.query_transformer.transform_query(question)
        logger.info(f"Transformed query: {better_question}")
        
        return {"documents": documents, "question": better_question}
    
    def generate(self, state: GraphState) -> Dict[str, Any]:
        """
        Generate response based on documents.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with generation
        """
        logger.info("Node: GENERATE")
        question = state["question"]
        documents = state["documents"]
        
        # Generate response
        generation = self.generator.generate(question, documents)
        
        return {
            "documents": documents, 
            "question": question, 
            "generation": generation
        }