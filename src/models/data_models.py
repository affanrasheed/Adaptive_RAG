"""Data models for Adaptive RAG."""

from typing import List, Literal, Optional, Dict, Any
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain.schema import Document

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "web_search"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )

class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: Original user question
        generation: LLM generation/response
        documents: List of retrieved documents
    """

    question: str
    generation: Optional[str]
    documents: Optional[List[Document]]

class WebSearchResult(TypedDict):
    """Structure for web search results."""
    
    content: str
    title: Optional[str]
    url: Optional[str]

class RAGResult(BaseModel):
    """Result from the RAG system."""
    
    question: str
    answer: str
    documents: List[Document]
    routing_decision: str
    transformations: List[str] = Field(default_factory=list)
    search_results: Optional[List[WebSearchResult]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)