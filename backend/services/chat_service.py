"""
Chat Service - Main Orchestration
Coordinates RAG, LLM, and conversation logic for the AI SDR.
"""

from services.rag_service import get_rag_service
from services.llm_service import get_llm_service
from prompts.system_prompt import get_system_prompt
from prompts.product_info import get_product_names
from models.schemas import Message, QuickReply, Source


class ChatService:
    """Main service for handling chat conversations."""
    
    def __init__(self):
        """Initialize chat service with RAG and LLM services."""
        self.rag_service = get_rag_service()
        self.llm_service = get_llm_service(self.rag_service)
        self.system_prompt = get_system_prompt()
    
    def get_initial_greeting(self) -> dict:
        """
        Get the initial greeting for a new conversation.
        
        Returns:
            Dict with response and optional quick_replies
        """
        greeting = (
            "Hi! I'm Alex, an AI assistant with EliseAI. "
            "We help property management and healthcare organizations automate operations "
            "and improve efficiency with AI-powered solutions. "
            "\n\nWhat brings you here today - are you in property management, healthcare, "
            "or something else?"
        )
        
        return {
            "response": greeting,
            "quick_replies": None,  # No buttons on first message
            "sources": [],
            "tool_used": None,
            "calendly_url": None
        }
    
    def should_show_product_buttons(self, messages: list[Message]) -> bool:
        """
        Determine if we should show product selection buttons.
        
        Show buttons on the 2nd AI response if:
        - User hasn't mentioned a specific product yet
        - Conversation is still in early stage
        
        Args:
            messages: Conversation history
        
        Returns:
            True if product buttons should be shown
        """
        # Count assistant messages (excluding system prompt)
        assistant_count = sum(1 for m in messages if m.role == "assistant")
        
        # Only show on 2nd assistant message
        if assistant_count != 1:
            return False
        
        # Check if user has mentioned specific products
        product_names = get_product_names()
        user_messages = [m.content.lower() for m in messages if m.role == "user"]
        
        for msg in user_messages:
            for product in product_names:
                if product.lower() in msg:
                    return False  # They've already focused on a product
        
        return True
    
    def get_product_quick_replies(self) -> list[QuickReply]:
        """Get quick reply buttons for product selection."""
        return [
            QuickReply(label="🏢 LeasingAI", value="Tell me about LeasingAI"),
            QuickReply(label="🔧 MaintenanceAI", value="Tell me about MaintenanceAI"),
            QuickReply(label="💰 DelinquencyAI", value="Tell me about DelinquencyAI"),
            QuickReply(label="📋 LeaseAudits", value="Tell me about LeaseAudits"),
            QuickReply(label="📊 EliseCRM", value="Tell me about EliseCRM"),
            QuickReply(label="💬 Discuss my needs", value="I'd like to discuss my specific challenges")
        ]
    
    def handle_message(self, messages: list[Message]) -> dict:
        """
        Handle an incoming message and generate a response.
        
        Args:
            messages: Full conversation history
        
        Returns:
            Dict with response, quick_replies, sources, etc.
        """
        # Build conversation for LLM (system prompt + messages)
        llm_messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        for msg in messages:
            llm_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Get response from LLM (with potential tool calls)
        llm_result = self.llm_service.chat_completion(llm_messages)
        
        # Prepare response
        response = {
            "response": llm_result["response"],
            "sources": [
                Source(
                    title=source["title"],
                    author=source["author"],
                    date=source["date"]
                )
                for source in llm_result.get("sources", [])
            ],
            "tool_used": llm_result.get("tool_used"),
            "quick_replies": None,
            "calendly_url": None
        }
        
        # Add Calendly link if demo was booked
        if llm_result.get("tool_used") == "book_demo":
            tool_result = llm_result.get("tool_result", {})
            response["calendly_url"] = tool_result.get("calendly_url")
        
        # Add product buttons if appropriate
        if self.should_show_product_buttons(messages):
            response["quick_replies"] = self.get_product_quick_replies()
        
        return response


# Singleton instance
_chat_service_instance = None


def get_chat_service() -> ChatService:
    """Get or create chat service singleton."""
    global _chat_service_instance
    if _chat_service_instance is None:
        _chat_service_instance = ChatService()
    return _chat_service_instance

