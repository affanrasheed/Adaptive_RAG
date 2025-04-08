"""Grading components for Adaptive RAG."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from typing import List

from ..models.data_models import GradeDocuments, GradeHallucinations, GradeAnswer

class DocumentGrader:
    """Grades document relevance to a question."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize document grader.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.structured_llm = self.llm.with_structured_output(GradeDocuments)
        
        # Define the grader prompt
        system_prompt = """You are a grader assessing relevance of a retrieved document to a user question. 
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. 
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
            ]
        )
        
        # Create the grading chain
        self.grader_chain = self.prompt | self.structured_llm
        
    def grade_document(self, document: Document, question: str) -> bool:
        """
        Grade a document's relevance to a question.
        
        Args:
            document: Document to grade
            question: User question
            
        Returns:
            True if the document is relevant, False otherwise
        """
        result = self.grader_chain.invoke({
            "document": document.page_content,
            "question": question
        })
        return result.binary_score.lower() == "yes"
    
    def filter_documents(self, documents: List[Document], question: str) -> List[Document]:
        """
        Filter a list of documents based on relevance.
        
        Args:
            documents: List of documents to filter
            question: User question
            
        Returns:
            Filtered list of relevant documents
        """
        return [doc for doc in documents if self.grade_document(doc, question)]


class HallucinationGrader:
    """Grades whether a generation is grounded in the provided documents."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize hallucination grader.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.structured_llm = self.llm.with_structured_output(GradeHallucinations)
        
        # Define the grader prompt
        system_prompt = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
        Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
            ]
        )
        
        # Create the grading chain
        self.grader_chain = self.prompt | self.structured_llm
        
    def grade_generation(self, documents: List[Document], generation: str) -> bool:
        """
        Grade whether a generation is grounded in the provided documents.
        
        Args:
            documents: Documents that should ground the generation
            generation: Generated text to grade
            
        Returns:
            True if the generation is grounded, False otherwise
        """
        # Combine document content
        docs_content = "\n\n".join([doc.page_content for doc in documents])
        
        result = self.grader_chain.invoke({
            "documents": docs_content,
            "generation": generation
        })
        return result.binary_score.lower() == "yes"


class AnswerGrader:
    """Grades whether a generation addresses the original question."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize answer grader.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.structured_llm = self.llm.with_structured_output(GradeAnswer)
        
        # Define the grader prompt
        system_prompt = """You are a grader assessing whether an answer addresses / resolves a question.
        Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
            ]
        )
        
        # Create the grading chain
        self.grader_chain = self.prompt | self.structured_llm
        
    def grade_answer(self, question: str, generation: str) -> bool:
        """
        Grade whether a generation addresses the original question.
        
        Args:
            question: Original user question
            generation: Generated text to grade
            
        Returns:
            True if the generation addresses the question, False otherwise
        """
        result = self.grader_chain.invoke({
            "question": question,
            "generation": generation
        })
        return result.binary_score.lower() == "yes"