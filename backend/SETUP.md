# Backend Setup Guide

## Phase 1 Complete! ✅

All backend files have been created. Follow these steps to get it running:

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Configure Environment

Make sure your `.env` file contains:

```env
OPENAI_API_KEY=your_key_here
```

## Step 3: Run Article Ingestion (ONE TIME ONLY)

This loads all 92 articles into ChromaDB:

```bash
python scripts/ingest_articles.py
```

Expected output:
- ✅ 92 articles loaded
- ✅ ~XXX chunks created
- ✅ Vector store created

## Step 4: Start the Backend

```bash
python app.py
```

Backend will be available at: http://localhost:8000

## Test the API

```bash
# Health check
curl http://localhost:8000/api/

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "session_id": "test123"
  }'
```

## Project Structure

```
backend/
├── app.py                     # ✅ Main FastAPI app
├── config.py                  # ✅ Settings management
├── models/
│   └── schemas.py             # ✅ Request/response models
├── services/
│   ├── chat_service.py        # ✅ Main orchestration
│   ├── rag_service.py         # ✅ Vector search
│   └── llm_service.py         # ✅ OpenAI integration
├── tools/
│   └── tool_definitions.py    # ✅ Function calling tools
├── prompts/
│   ├── system_prompt.py       # ✅ SDR behavior
│   └── product_info.py        # ✅ Product descriptions
└── scripts/
    └── ingest_articles.py     # ✅ Data ingestion
```

## What's Next?

Phase 1 (Backend) is COMPLETE! ✅

Ready for Phase 2 (Frontend) whenever you are!

