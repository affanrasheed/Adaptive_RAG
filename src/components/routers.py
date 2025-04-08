"""Query routing components for Adaptive RAG."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ..models.data_models import RouteQuery

class QueryRouter:
    """Routes queries to the appropriate data source."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize query router.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for model generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.structured_llm = self.llm.with_structured_output(RouteQuery)
        
        # Define the router prompt
        system_prompt = """You are an expert at routing a user question to a vectorstore or web search.
        The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
        Use the vectorstore for questions on these topics. Otherwise, use web-search.
        
        When deciding, consider:
        1. Is the question about a specific topic in the vectorstore?
        2. Is the question asking for recent information or news?
        3. Is the question about a specialized domain not likely covered in the vectorstore?
        """
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{question}"),
            ]
        )
        
        # Create the routing chain
        self.router_chain = self.prompt | self.structured_llm
        
    def route(self, question: str) -> str:
        """
        Route a query to the appropriate source.
        
        Args:
            question: User question
            
        Returns:
            Data source to use ("vectorstore" or "web_search")
        """
        result = self.router_chain.invoke({"question": question})
        return result.datasource
    
    def update_vectorstore_topics(self, topics: str) -> None:
        """
        Update the prompt with the current topics in the vectorstore.
        
        Args:
            topics: Description of topics in the vectorstore
        """
        system_prompt = f"""You are an expert at routing a user question to a vectorstore or web search.
        The vectorstore contains documents related to: {topics}.
        Use the vectorstore for questions on these topics. Otherwise, use web-search.
        
        When deciding, consider:
        1. Is the question about a specific topic in the vectorstore?
        2. Is the question asking for recent information or news?
        3. Is the question about a specialized domain not likely covered in the vectorstore?
        """
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{question}"),
            ]
        )
        
        # Update the routing chain
        self.router_chain = self.prompt | self.structured_llm