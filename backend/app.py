"""
FastAPI Application - AI SDR Chatbot
Main entry point with API routes.
"""

from fastapi import FastAPI, Body, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models.schemas import (
    ChatRequest,
    ChatResponse,
    InitChatRequest,
    InitChatResponse
)
from services.chat_service import get_chat_service

app = FastAPI(title="EliseAI SDR Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")


@api_router.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": "EliseAI SDR Chatbot API",
        "status": "running",
        "version": "1.0.0"
    }


@api_router.post("/chat/init", response_model=InitChatResponse)
def init_chat(request: InitChatRequest):
    """
    Initialize a new chat session with an initial greeting.
    
    Args:
        request: Init chat request with session_id
    
    Returns:
        Initial greeting and setup info
    """
    try:
        chat_service = get_chat_service()
        greeting = chat_service.get_initial_greeting()
        
        return InitChatResponse(
            response=greeting["response"],
            quick_replies=greeting.get("quick_replies"),
            is_new_session=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing chat: {str(e)}")


@api_router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint - handles conversation with the AI SDR.
    
    This endpoint is stateless - the client sends the full conversation history
    with each request.
    
    Args:
        request: Chat request with messages and session_id
    
    Returns:
        AI response with optional quick replies and sources
    """
    try:
        chat_service = get_chat_service()
        result = chat_service.handle_message(request.messages)
        
        return ChatResponse(
            response=result["response"],
            quick_replies=result.get("quick_replies"),
            sources=result.get("sources"),
            tool_used=result.get("tool_used"),
            calendly_url=result.get("calendly_url")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
