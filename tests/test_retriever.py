"""Tests for retriever components."""

import unittest
from unittest.mock import MagicMock, patch
from langchain.schema import Document

from src.components.retrievers import VectorStoreRetriever, HybridRetriever

class TestVectorStoreRetriever(unittest.TestCase):
    """Test the VectorStoreRetriever component."""
    
    @patch('src.components.retrievers.Chroma')
    @patch('src.components.retrievers.OpenAIEmbeddings')
    def test_init(self, mock_embeddings, mock_chroma):
        """Test initialization."""
        # Set up mocks
        mock_embeddings.return_value = MagicMock()
        mock_chroma.return_value = MagicMock()
        mock_chroma.return_value.as_retriever.return_value = MagicMock()
        
        # Create retriever
        retriever = VectorStoreRetriever(
            collection_name="test-collection",
            search_kwargs={"k": 2}
        )
        
        # Assertions
        self.assertEqual(retriever.collection_name, "test-collection")
        self.assertEqual(retriever.search_kwargs, {"k": 2})
        mock_chroma.assert_called_once()
        mock_embeddings.assert_called_once()
    
    @patch('src.components.retrievers.Chroma')
    @patch('src.components.retrievers.OpenAIEmbeddings')
    def test_retrieve(self, mock_embeddings, mock_chroma):
        """Test retrieve method."""
        # Set up mocks
        mock_embeddings.return_value = MagicMock()
        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = [
            Document(page_content="Test content", metadata={"source": "test"})
        ]
        mock_chroma.return_value = MagicMock()
        mock_chroma.return_value.as_retriever.return_value = mock_retriever
        
        # Create retriever
        retriever = VectorStoreRetriever()
        
        # Test retrieve
        docs = retriever.retrieve("test query")
        
        # Assertions
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].page_content, "Test content")
        mock_retriever.invoke.assert_called_once_with("test query")

class TestHybridRetriever(unittest.TestCase):
    """Test the HybridRetriever component."""
    
    def test_init(self):
        """Test initialization."""
        # Create mock retrievers
        retriever1 = MagicMock()
        retriever2 = MagicMock()
        
        # Create hybrid retriever
        hybrid = HybridRetriever(
            retrievers=[retriever1, retriever2],
            weights=[0.7, 0.3]
        )
        
        # Assertions
        self.assertEqual(len(hybrid.retrievers), 2)
        self.assertEqual(hybrid.weights, [0.7, 0.3])
    
    def test_retrieve(self):
        """Test retrieve method."""
        # Create mock retrievers
        retriever1 = MagicMock()
        retriever1.invoke.return_value = [
            Document(page_content="Doc1", metadata={"score": 0.9, "source": "retriever1"})
        ]
        
        retriever2 = MagicMock()
        retriever2.invoke.return_value = [
            Document(page_content="Doc2", metadata={"score": 0.8, "source": "retriever2"})
        ]
        
        # Create hybrid retriever
        hybrid = HybridRetriever(
            retrievers=[retriever1, retriever2],
            weights=[0.7, 0.3]
        )
        
        # Test retrieve
        docs = hybrid.retrieve("test query", limit=2)
        
        # Assertions
        self.assertEqual(len(docs), 2)
        retriever1.invoke.assert_called_once_with("test query")
        retriever2.invoke.assert_called_once_with("test query")
        
        # Check metadata is updated correctly
        self.assertTrue("retriever" in docs[0].metadata)
        self.assertTrue("retriever" in docs[1].metadata)

if __name__ == '__main__':
    unittest.main()