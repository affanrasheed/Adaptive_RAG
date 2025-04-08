"""Document loading and indexing utilities."""

from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

def load_documents_from_urls(urls: List[str]) -> List[Document]:
    """
    Load documents from a list of URLs.
    
    Args:
        urls: List of URLs to load
        
    Returns:
        List of loaded documents
    """
    docs = []
    for url in urls:
        try:
            url_docs = WebBaseLoader(url).load()
            docs.extend(url_docs)
        except Exception as e:
            print(f"Error loading {url}: {e}")
    
    return docs

def split_documents(
    documents: List[Document], 
    chunk_size: int = 500, 
    chunk_overlap: int = 0
) -> List[Document]:
    """
    Split documents into chunks.
    
    Args:
        documents: List of documents to split
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of split documents
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def create_vectorstore(
    documents: List[Document],
    collection_name: str = "adaptive-rag-collection",
    embedding_model: Optional[str] = None,
) -> Chroma:
    """
    Create a vectorstore from documents.
    
    Args:
        documents: Documents to index
        collection_name: Name for the Chroma collection
        embedding_model: Optional specific OpenAI embedding model to use
        
    Returns:
        Chroma vectorstore
    """
    # Set up embeddings
    embedding_kwargs = {}
    if embedding_model:
        embedding_kwargs["model"] = embedding_model
        
    embeddings = OpenAIEmbeddings(**embedding_kwargs)
    
    # Create and return the vectorstore
    return Chroma.from_documents(
        documents=documents,
        collection_name=collection_name,
        embedding=embeddings,
    )

def load_and_index_urls(
    urls: List[str],
    collection_name: str = "adaptive-rag-collection",
    chunk_size: int = 500,
    chunk_overlap: int = 0,
    embedding_model: Optional[str] = None,
) -> Chroma:
    """
    Load documents from URLs, split them, and create a vectorstore.
    
    Args:
        urls: URLs to load
        collection_name: Name for the Chroma collection
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        embedding_model: Optional specific OpenAI embedding model to use
        
    Returns:
        Chroma vectorstore
    """
    # Load documents
    documents = load_documents_from_urls(urls)
    
    # Split documents
    split_docs = split_documents(
        documents, 
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    
    # Create vectorstore
    return create_vectorstore(
        split_docs,
        collection_name=collection_name,
        embedding_model=embedding_model,
    )