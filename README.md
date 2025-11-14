# EliseAI SDR Chatbot - AI-Powered Sales Assistant

An intelligent, conversational AI Sales Development Representative that leverages Retrieval-Augmented Generation (RAG) to answer questions about EliseAI's products using knowledge from 92 blog articles, and seamlessly guides prospects toward booking demos.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd full-stack-eng-practical-main
   ```

2. **Configure API Key**
   
   Add your OpenAI API key to `backend/.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the Application**
   ```bash
   docker-compose up --build
   ```
   This will start:
   - Backend API on http://localhost:8000
   - Frontend UI on http://localhost:3000
   - SQLite database initialization

4. **Initialize Knowledge Base (One-Time)**
   
   In a separate terminal, run the article ingestion script:
   ```bash
   docker exec -it backend-practical python scripts/ingest_articles.py
   ```
   
   This processes 92 blog articles into 836 searchable chunks with embeddings (~2-3 minutes).

5. **Access the Application**
   
   Open your browser to **http://localhost:3000** and start chatting!

---

## Architecture & Approach

### Design Philosophy

I designed this system to keep in mind: modularity for maintainability, stateless architecture for scalability, optimized RAG for performance, and clean separation of concerns for code quality.

### System Architecture

```
Frontend (React + TypeScript)
    ↓
Stateless REST API (FastAPI)
    ↓
├── Chat Service (Orchestration)
├── RAG Service (ChromaDB Vector Search)
├── LLM Service (OpenAI GPT-4o-mini + Function Calling)
└── Tool Handlers (search_kb, book_demo)
    ↓
├── ChromaDB (836 embedded article chunks)
└── SQLite (Demo request storage)
```

### Key Technical Decisions

#### 1. **Modular Service Architecture**
The backend is organized into distinct, swappable services:
- **`chat_service.py`**: Orchestrates conversation flow and tool usage
- **`rag_service.py`**: Handles semantic search (can easily swap ChromaDB for Pinecone/Weaviate)
- **`llm_service.py`**: Manages OpenAI integration (can swap for Claude, local models, etc.)
- **`prompt_service.py`**: Centralizes prompt management for easy iteration

This separation of concerns means changing the vector database or LLM provider requires modifying just one file, not the entire codebase.

#### 2. **Stateless Backend for Horizontal Scalability**
The API is completely stateless—each request includes full conversation context. This enables:
- Easy horizontal scaling (spin up multiple instances)
- Load balancer compatibility
- No session synchronization complexity
- Cloud-native deployment readiness

#### 3. **Optimized RAG Pipeline**
- **Chunking Strategy**: 1000 characters with 200-character overlap balances context retention with granularity -- modable in config
- **Embedding Model**: `text-embedding-3-small` provides 99% of quality at 10x lower cost than `text-embedding-3-large`
- **Top-K Retrieval**: Configured to retrieve only 3 most relevant chunks, minimizing token usage while maintaining accuracy
- **ChromaDB with HNSW**: Sub-100ms similarity search on 836 document chunks

#### 4. **OpenAI Function Calling**
Implements two tools via function calling:
- **`search_knowledge_base`**: Semantic search when the AI needs specific product information
- **`book_demo`**: Provides Calendly link when prospect is ready to schedule

The AI intelligently decides when to use tools based on conversation context, avoiding unnecessary API calls.

#### 5. **Session Persistence Without Authentication**
Uses browser `localStorage` for session management:
- Conversations persist across page refreshes
- No authentication complexity for a demo-focused tool
- Privacy-friendly (data stays client-side)
- Easy to upgrade to authenticated sessions later

### Tech Stack

**Backend:**
- Python 3.9
- FastAPI (async-capable REST API)
- LangChain (RAG orchestration)
- ChromaDB (vector database)
- OpenAI API (GPT-4o-mini + embeddings)
- SQLite (structured data storage)
- Pydantic (request validation)

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS (modern, responsive UI)
- Vite (fast builds and hot reload)
- localStorage (client-side persistence)

**Infrastructure:**
- Docker + Docker Compose
- Multi-stage builds for optimization

---

## Notable Challenges & Solutions

### Challenge 1: Time Constraints & Feature Prioritization

**Problem**: With limited time, I needed to balance building core functionality (RAG, chat, demo booking) with polish (UI enhancements, error handling, form integration).

**Solution**: I prioritized in phases:
1. **Phase 1 (Backend)**: Core RAG pipeline, system prompt engineering, tool definitions 
2. **Phase 2 (Rag Processing)**; Processing docs into the RAG (ChromaDB)
2. **Phase 3 (Frontend)**: Functional chat UI with session management 
3. **Phase 4 (Polish)**: Multi-line input, typing indicators, clear chat, demo form, etc

This phased approach ensured I had a working MVP early, then iteratively enhanced UX. The modular architecture made it easy to add features without refactoring.

### Challenge 2: RAG Quality vs. Performance Trade-offs

**Problem**: Finding the right balance between context quality (retrieving enough relevant information) and performance (API cost, latency, token limits).

**Solution**: 
- Landed on **1000 characters** as the sweet spot
- Implemented **200-character overlap** to prevent context loss at chunk boundaries
- Set **top-k=3** to retrieve only the most relevant chunks, reducing GPT-4o-mini input tokens by ~70%
- Used the **smaller embedding model** (`text-embedding-3-small`) which maintained 99% accuracy while being 10x cheaper

**Result**: Sub-100ms RAG queries, average of 2,000 tokens per conversation turn (well within budget).


---

## How I'd Improve With More Time

 1. Monitoring to determine when and what chats lead to bookings
 2. Integration with full EliseAI website
 3. Auth
 4. Sounding more human; ie: not using ** in responses
 5. Alex gives option of collecting info for user and booking herself, vs giving user form similar to website, instead of current calendly trigger