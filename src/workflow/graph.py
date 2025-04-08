"""Workflow graph for Adaptive RAG."""

from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, Optional
import logging

from ..models.data_models import GraphState
from .nodes import WorkflowNodes
from .edges import WorkflowEdges

logger = logging.getLogger(__name__)

class AdaptiveRAGWorkflow:
    """Workflow graph for Adaptive RAG."""
    
    def __init__(
        self,
        nodes: WorkflowNodes,
        edges: WorkflowEdges,
        debug: bool = False,
    ):
        """
        Initialize the workflow graph.
        
        Args:
            nodes: Workflow node functions
            edges: Workflow edge functions
            debug: Whether to enable debug logging
        """
        self.nodes = nodes
        self.edges = edges
        
        # Set up logging
        if debug:
            logging.basicConfig(level=logging.INFO)
        
        # Build the graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the workflow graph.
        
        Returns:
            Compiled workflow graph
        """
        # Create the graph
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("retrieve", self.nodes.retrieve)
        workflow.add_node("web_search", self.nodes.web_search)
        workflow.add_node("grade_documents", self.nodes.grade_documents)
        workflow.add_node("transform_query", self.nodes.transform_query)
        workflow.add_node("generate", self.nodes.generate)
        
        # Add edges
        workflow.add_conditional_edges(
            START,
            self.edges.route_question,
            {
                "web_search": "web_search",
                "vectorstore": "retrieve",
            },
        )
        workflow.add_edge("web_search", "generate")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            self.edges.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "retrieve")
        workflow.add_conditional_edges(
            "generate",
            self.edges.grade_generation,
            {
                "not_supported": "generate",
                "useful": END,
                "not_useful": "transform_query",
            },
        )
        
        return workflow
    
    def run(self, question: str) -> Dict[str, Any]:
        """
        Run the workflow with a question.
        
        Args:
            question: User question
            
        Returns:
            Final state of the workflow
        """
        # Initialize state
        state = {"question": question}
        
        # Run the workflow
        final_state = self.app.invoke(state)
        
        return final_state
    
    def stream(self, question: str):
        """
        Stream the workflow execution with a question.
        
        Args:
            question: User question
            
        Yields:
            Intermediate states of the workflow
        """
        # Initialize state
        state = {"question": question}
        
        # Stream the workflow execution
        return self.app.stream(state)