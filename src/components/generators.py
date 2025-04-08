"""Generation components for Adaptive RAG."""

from typing import List, Optional
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.schema import Document

class RAGGenerator:
    """Component for generating responses from retrieved documents."""
    
    def __init__(
        self, 
        model_name: str = "gpt-4o-mini",
        temperature: float = 0,
        prompt_template: Optional[str] = None,
    ):
        """
        Initialize RAG generator.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for generation
            prompt_template: Optional custom prompt template
        """
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        
        # Use provided prompt or pull from LangChain hub
        if prompt_template:
            self.prompt = ChatPromptTemplate.from_template(prompt_template)
        else:
            try:
                self.prompt = hub.pull("rlm/rag-prompt")
            except:
                # Fallback if hub pull fails
                default_template = """
                You are a helpful assistant that answers questions based on the provided context.
                
                Context:
                {context}
                
                Question:
                {question}
                
                Answer the question based on the context provided. If the context doesn't contain relevant information, say so, but try to provide a helpful response using your knowledge.
                """
                self.prompt = ChatPromptTemplate.from_template(default_template)
        
        # Create the generation chain
        self.generation_chain = self.prompt | self.llm | StrOutputParser()
        
    def _format_docs(self, docs: List[Document]) -> str:
        """Format a list of documents into a string context."""
        return "\n\n".join(doc.page_content for doc in docs)
        
    def generate(self, question: str, documents: List[Document]) -> str:
        """
        Generate a response based on retrieved documents.
        
        Args:
            question: User question
            documents: Retrieved documents
            
        Returns:
            Generated response
        """
        # Format documents into context string
        context = self._format_docs(documents)
        
        # Generate response
        return self.generation_chain.invoke({
            "context": context,
            "question": question
        })