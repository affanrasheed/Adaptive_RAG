"""Setup script for the Adaptive RAG package."""

from setuptools import setup, find_packages

setup(
    name="adaptive_rag",
    version="0.1.0",
    description="Adaptive Retrieval Augmented Generation system",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "langchain-community>=0.0.11",
        "langgraph>=0.0.20",
        "openai>=1.6.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "tiktoken>=0.5.2",
        "tavily-python>=0.2.8",
        "chromadb>=0.4.18",
        "typing-extensions>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "jupyter>=1.0.0",
        ],
    },
    python_requires=">=3.9",
)