"""
RAG Service - Retrieval Augmented Generation
Handles semantic search over the EliseAI blog articles using ChromaDB.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import get_settings


class RAGService:
    """Service for retrieving relevant content from the knowledge base."""
    
    def __init__(self):
        """Initialize the RAG service with ChromaDB connection."""
        import os
        self.settings = get_settings()
        
        # Set API key in environment for OpenAI
        os.environ["OPENAI_API_KEY"] = self.settings.openai_api_key
        
        self.embeddings = OpenAIEmbeddings(
            model=self.settings.embedding_model
        )
        
        # Load existing vector store
        self.vectorstore = Chroma(
            persist_directory=self.settings.chroma_persist_directory,
            embedding_function=self.embeddings,
            collection_name="eliseai_articles"
        )
    
    def search(self, query: str, top_k: int = None) -> list[dict]:
        """
        Search the knowledge base for relevant content.
        
        Args:
            query: Search query string
            top_k: Number of results to return (defaults to settings.rag_top_k)
        
        Returns:
            List of dicts with 'content' and 'metadata' keys
        """
        if top_k is None:
            top_k = self.settings.rag_top_k
        
        # Perform similarity search
        results = self.vectorstore.similarity_search(query, k=top_k)
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata
            })
        
        return formatted_results
    
    def format_results_for_llm(self, results: list[dict]) -> str:
        """
        Format search results into a string for LLM context.
        
        Args:
            results: List of search results from self.search()
        
        Returns:
            Formatted string with relevant articles
        """
        if not results:
            return "No relevant articles found."
        
        formatted = "## Relevant Knowledge Base Articles:\n\n"
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            content = result['content']
            
            formatted += f"### Article {i}: {metadata.get('title', 'Untitled')}\n"
            formatted += f"Author: {metadata.get('author', 'Unknown')} | Date: {metadata.get('date', 'N/A')}\n\n"
            formatted += f"{content}\n\n"
            formatted += "---\n\n"
        
        return formatted
    
    def get_source_citations(self, results: list[dict]) -> list[dict]:
        """
        Extract source citations from search results.
        
        Args:
            results: List of search results
        
        Returns:
            List of citation dicts with title, author, date
        """
        citations = []
        seen_titles = set()
        
        for result in results:
            metadata = result['metadata']
            title = metadata.get('title')
            
            # Avoid duplicate citations
            if title and title not in seen_titles:
                citations.append({
                    'title': title,
                    'author': metadata.get('author', 'Unknown'),
                    'date': metadata.get('date', 'N/A')
                })
                seen_titles.add(title)
        
        return citations


# Singleton instance
_rag_service_instance = None


def get_rag_service() -> RAGService:
    """Get or create RAG service singleton."""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance

