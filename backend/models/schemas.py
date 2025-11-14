"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")


class QuickReply(BaseModel):
    """A quick reply button option."""
    label: str = Field(..., description="Button label to display")
    value: str = Field(..., description="Message text to send when clicked")


class Source(BaseModel):
    """A source citation from the knowledge base."""
    title: str
    author: str
    date: str


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    messages: list[Message] = Field(..., description="Conversation history")
    session_id: Optional[str] = Field(None, description="Session identifier")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    response: str = Field(..., description="AI response text")
    quick_replies: Optional[list[QuickReply]] = Field(None, description="Optional quick reply buttons")
    sources: Optional[list[Source]] = Field(None, description="Knowledge base sources used")
    tool_used: Optional[str] = Field(None, description="Tool that was called, if any")
    calendly_url: Optional[str] = Field(None, description="Calendly link if demo was booked")


class InitChatRequest(BaseModel):
    """Request body for init chat endpoint."""
    session_id: str = Field(..., description="Session identifier")


class InitChatResponse(BaseModel):
    """Response from init chat endpoint."""
    response: str = Field(..., description="Initial greeting message")
    quick_replies: Optional[list[QuickReply]] = Field(None, description="Initial quick reply options")
    is_new_session: bool = Field(..., description="Whether this is a new session")

