"""Workflow edges (conditional logic) for Adaptive RAG."""

from typing import Dict, Any, Literal
from ..models.data_models import GraphState
from ..components.routers import QueryRouter
from ..components.graders import HallucinationGrader, AnswerGrader
import logging

logger = logging.getLogger(__name__)

class WorkflowEdges:
    """Contains all the edge decision functions for the workflow graph."""
    
    def __init__(
        self,
        query_router: QueryRouter,
        hallucination_grader: HallucinationGrader,
        answer_grader: AnswerGrader,
    ):
        """
        Initialize workflow edges.
        
        Args:
            query_router: Query routing component
            hallucination_grader: Hallucination grading component
            answer_grader: Answer grading component
        """
        self.query_router = query_router
        self.hallucination_grader = hallucination_grader
        self.answer_grader = answer_grader
    
    def route_question(self, state: GraphState) -> Literal["web_search", "vectorstore"]:
        """
        Route question to web search or vectorstore.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node to call ("web_search" or "vectorstore")
        """
        logger.info("Edge: ROUTE QUESTION")
        question = state["question"]
        
        # Route the question
        source = self.query_router.route(question)
        
        if source == "web_search":
            logger.info("Decision: Route to WEB SEARCH")
            return "web_search"
        else:
            logger.info("Decision: Route to VECTORSTORE")
            return "vectorstore"
    
    def decide_to_generate(self, state: GraphState) -> Literal["transform_query", "generate"]:
        """
        Decide whether to generate an answer or transform the query.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node to call ("transform_query" or "generate")
        """
        logger.info("Edge: ASSESS GRADED DOCUMENTS")
        filtered_documents = state["documents"]
        
        if not filtered_documents:
            # No relevant documents found, transform query
            logger.info("Decision: ALL DOCUMENTS ARE NOT RELEVANT, TRANSFORM QUERY")
            return "transform_query"
        else:
            # Generate response with relevant documents
            logger.info("Decision: GENERATE")
            return "generate"
    
    def grade_generation(
        self, state: GraphState
    ) -> Literal["useful", "not_useful", "not_supported"]:
        """
        Grade the generation for hallucinations and answer quality.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next action to take ("useful", "not_useful", or "not_supported")
        """
        logger.info("Edge: CHECK HALLUCINATIONS AND ANSWER QUALITY")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
       
        
        # Check for hallucinations
        is_grounded = self.hallucination_grader.grade_generation(documents, generation)
        
        if is_grounded:
            logger.info("Decision: GENERATION IS GROUNDED IN DOCUMENTS")
            
            # Check if generation addresses the question
            answers_question = self.answer_grader.grade_answer(question, generation)
            
            if answers_question:
                logger.info("Decision: GENERATION ADDRESSES QUESTION")
                return "useful"
            else:
                logger.info("Decision: GENERATION DOES NOT ADDRESS QUESTION")
                return "not_useful"
        else:
            logger.info("Decision: GENERATION IS NOT GROUNDED IN DOCUMENTS")
            return "not_supported"