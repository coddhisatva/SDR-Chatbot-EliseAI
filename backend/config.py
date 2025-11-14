"""
Configuration management for the EliseAI SDR chatbot.
Loads settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: str
    
    # Database paths
    database_url: str = "/data/practical.db"
    chroma_persist_directory: str = "/app/data/chroma_db"
    articles_directory: str = "/app/articles"
    
    # Application settings
    environment: str = "development"
    debug: bool = True
    
    # RAG settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_model: str = "text-embedding-3-small"
    rag_top_k: int = 3
    
    # LLM settings
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.7
    max_tokens: int = 800
    
    # Calendly
    calendly_demo_link: str = "https://calendly.com/eliseai-demo/30min"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

