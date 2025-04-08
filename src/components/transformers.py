"""Query transformation components for Adaptive RAG."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class QueryTransformer:
    """Transforms user queries to improve retrieval performance."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize query transformer.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        # Define the transformer prompt
        system_prompt = """You are a question re-writer that converts an input question to a better version that is optimized 
        for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning.
        
        Consider making these improvements:
        1. Add relevant synonyms or alternative phrasings
        2. Expand abbreviations or acronyms
        3. Remove filler words that don't add semantic meaning
        4. Break down complex questions into their core components
        5. Add specific context keywords that might match documents
        
        Only return the rewritten question, not an explanation.
        """
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    "Here is the initial question: \n\n {question} \n Formulate an improved question.",
                ),
            ]
        )
        
        # Create the transformation chain
        self.transform_chain = self.prompt | self.llm | StrOutputParser()
        
    def transform_query(self, question: str) -> str:
        """
        Transform a query to improve retrieval performance.
        
        Args:
            question: Original user question
            
        Returns:
            Transformed query
        """
        return self.transform_chain.invoke({"question": question})


class HypotheticalDocumentGenerator:
    """Generates hypothetical documents that would answer a user's question."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.4):
        """
        Initialize hypothetical document generator.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        # Define the generator prompt
        system_prompt = """You are an expert at generating hypothetical document fragments that would perfectly answer a user's question.
        
        Your task is to imagine you are looking at a perfect document that contains the exact information needed to answer the user's question completely.
        Write a detailed excerpt from this hypothetical document.
        
        For example:
        - For factual questions, create informative reference content
        - For how-to questions, create instructional content
        - For conceptual questions, create explanatory content
        
        Make the document detailed and specific, as if written by a subject matter expert.
        """
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    "Generate a hypothetical document fragment that would perfectly answer this question: \n\n{question}",
                ),
            ]
        )
        
        # Create the generation chain
        self.generation_chain = self.prompt | self.llm | StrOutputParser()
        
    def generate_document(self, question: str) -> str:
        """
        Generate a hypothetical document based on the question.
        
        Args:
            question: User question
            
        Returns:
            Generated hypothetical document
        """
        return self.generation_chain.invoke({"question": question})