"""
Article Ingestion Script
Loads all JSON articles, chunks them, generates embeddings, and stores in ChromaDB.
Run this once to populate the vector database.

Usage: python scripts/ingest_articles.py
"""

import json
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_settings


def load_articles(articles_dir: str) -> list[dict]:
    """Load all JSON articles from the articles directory."""
    articles = []
    articles_path = Path(articles_dir)
    
    if not articles_path.exists():
        print(f"❌ Articles directory not found: {articles_dir}")
        return articles
    
    json_files = list(articles_path.glob("*.json"))
    print(f"📂 Found {len(json_files)} article files")
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                article = json.load(f)
                articles.append(article)
        except Exception as e:
            print(f"⚠️  Error loading {file_path.name}: {e}")
    
    print(f"✅ Successfully loaded {len(articles)} articles")
    return articles


def chunk_articles(articles: list[dict], chunk_size: int, chunk_overlap: int) -> tuple[list[str], list[dict]]:
    """
    Chunk article content and prepare metadata.
    Returns: (chunks, metadata_list)
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    all_metadata = []
    
    for article in articles:
        # Extract content
        title = article.get('title', 'Untitled')
        author = article.get('author', 'Unknown')
        date = article.get('date', 'N/A')
        summary = article.get('summary', '')
        content = article.get('main_content', '')
        
        # Combine summary and content for chunking
        full_text = f"# {title}\n\n{summary}\n\n{content}"
        
        # Split into chunks
        chunks = text_splitter.split_text(full_text)
        
        # Create metadata for each chunk
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                'title': title,
                'author': author,
                'date': date,
                'chunk_index': i,
                'total_chunks': len(chunks)
            })
    
    print(f"✅ Created {len(all_chunks)} chunks from {len(articles)} articles")
    return all_chunks, all_metadata


def create_vector_store(chunks: list[str], metadata: list[dict], settings) -> Chroma:
    """Create and populate ChromaDB vector store."""
    print("🔄 Initializing embeddings model...")
    
    # Set API key in environment for OpenAI
    import os
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model
    )
    
    print(f"🔄 Creating vector store at: {settings.chroma_persist_directory}")
    print("⏳ This may take a few minutes...")
    
    # Create the vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata,
        persist_directory=settings.chroma_persist_directory,
        collection_name="eliseai_articles"
    )
    
    print(f"✅ Vector store created successfully with {len(chunks)} chunks!")
    return vectorstore


def main():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("EliseAI Article Ingestion Script")
    print("=" * 60)
    
    # Load settings
    settings = get_settings()
    
    print(f"\n📋 Configuration:")
    print(f"  Articles directory: {settings.articles_directory}")
    print(f"  ChromaDB directory: {settings.chroma_persist_directory}")
    print(f"  Chunk size: {settings.chunk_size}")
    print(f"  Chunk overlap: {settings.chunk_overlap}")
    print(f"  Embedding model: {settings.embedding_model}\n")
    
    # Step 1: Load articles
    print("Step 1: Loading articles...")
    articles = load_articles(settings.articles_directory)
    
    if not articles:
        print("❌ No articles found. Exiting.")
        return
    
    # Step 2: Chunk articles
    print("\nStep 2: Chunking articles...")
    chunks, metadata = chunk_articles(
        articles,
        settings.chunk_size,
        settings.chunk_overlap
    )
    
    # Step 3: Create vector store
    print("\nStep 3: Creating vector store...")
    vectorstore = create_vector_store(chunks, metadata, settings)
    
    print("\n" + "=" * 60)
    print("✅ INGESTION COMPLETE!")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"  - {len(articles)} articles processed")
    print(f"  - {len(chunks)} chunks created")
    print(f"  - Vector store ready at: {settings.chroma_persist_directory}")
    print("\n🚀 Your RAG system is ready to use!")


if __name__ == "__main__":
    main()

