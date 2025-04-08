"""Tests for router components."""

import unittest
from unittest.mock import MagicMock, patch

from src.components.routers import QueryRouter
from src.models.data_models import RouteQuery

class TestQueryRouter(unittest.TestCase):
    """Test the QueryRouter component."""
    
    @patch('src.components.routers.ChatOpenAI')
    @patch('src.components.routers.ChatPromptTemplate')
    def test_init(self, mock_prompt, mock_llm):
        """Test initialization."""
        # Set up mocks
        mock_llm.return_value = MagicMock()
        mock_llm.return_value.with_structured_output.return_value = MagicMock()
        mock_prompt.from_messages.return_value = MagicMock()
        
        # Create router
        router = QueryRouter(model_name="test-model", temperature=0.2)
        
        # Assertions
        mock_llm.assert_called_once_with(model="test-model", temperature=0.2)
        mock_prompt.from_messages.assert_called_once()
    
    @patch('src.components.routers.ChatOpenAI')
    @patch('src.components.routers.ChatPromptTemplate')
    def test_route(self, mock_prompt, mock_llm):
        """Test route method."""
        # Set up mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = RouteQuery(datasource="vectorstore")
        
        mock_structured_llm = MagicMock()
        mock_llm.return_value = MagicMock()
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm
        
        mock_prompt_chain = MagicMock()
        mock_prompt.from_messages.return_value = mock_prompt_chain
        
        # Create router chain manually
        mock_prompt_chain.__or__.return_value = mock_chain
        
        # Create router
        router = QueryRouter()
        
        # Test route
        result = router.route("What are agents in LLMs?")
        
        # Assertions
        self.assertEqual(result, "vectorstore")
        mock_chain.invoke.assert_called_once_with({"question": "What are agents in LLMs?"})
    
    @patch('src.components.routers.ChatOpenAI')
    @patch('src.components.routers.ChatPromptTemplate')
    def test_update_vectorstore_topics(self, mock_prompt, mock_llm):
        """Test update_vectorstore_topics method."""
        # Set up mocks
        mock_structured_llm = MagicMock()
        mock_llm.return_value = MagicMock()
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm
        
        mock_prompt_chain = MagicMock()
        mock_prompt.from_messages.return_value = mock_prompt_chain
        
        # Create router
        router = QueryRouter()
        
        # Test update_vectorstore_topics
        router.update_vectorstore_topics("new topics")
        
        # Assertions
        # Check that a new prompt was created with the updated topics
        mock_prompt.from_messages.call_count >= 2

if __name__ == '__main__':
    unittest.main()