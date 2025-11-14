"""
LLM Service - OpenAI Integration
Handles all interactions with OpenAI's API including function calling.
"""

from openai import OpenAI
import json
from config import get_settings
from tools.tool_definitions import get_tool_definitions


class LLMService:
    """Service for interacting with OpenAI's API."""
    
    def __init__(self, rag_service):
        """
        Initialize the LLM service.
        
        Args:
            rag_service: RAGService instance for tool execution
        """
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.rag_service = rag_service
        self.tools = get_tool_definitions()
    
    def chat_completion(
        self,
        messages: list[dict],
        use_tools: bool = True
    ) -> dict:
        """
        Get a chat completion from OpenAI, handling function calls if needed.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            use_tools: Whether to enable function calling
        
        Returns:
            Dict with:
                - response: Final AI response text
                - tool_used: Name of tool if one was used
                - tool_result: Result from tool execution
                - sources: List of source citations if RAG was used
        """
        # Prepare messages
        conversation = messages.copy()
        
        # Make initial API call
        completion_kwargs = {
            "model": self.settings.llm_model,
            "messages": conversation,
            "temperature": self.settings.llm_temperature,
            "max_tokens": self.settings.max_tokens
        }
        
        if use_tools:
            completion_kwargs["tools"] = self.tools
            completion_kwargs["tool_choice"] = "auto"
        
        response = self.client.chat.completions.create(**completion_kwargs)
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        result = {
            "response": None,
            "tool_used": None,
            "tool_result": None,
            "sources": []
        }
        
        # If no tool calls, return the response directly
        if not tool_calls:
            result["response"] = response_message.content
            return result
        
        # Handle tool calls
        conversation.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            result["tool_used"] = function_name
            
            # Execute the appropriate tool
            if function_name == "search_knowledge_base":
                tool_response = self._execute_search_kb(function_args)
                result["tool_result"] = tool_response
                result["sources"] = tool_response.get("citations", [])
                
                # Add tool response to conversation
                conversation.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_response["formatted_content"]
                })
            
            elif function_name == "book_demo":
                tool_response = self._execute_book_demo(function_args)
                result["tool_result"] = tool_response
                
                # Add tool response to conversation
                conversation.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_response)
                })
        
        # Get final response after tool execution
        final_response = self.client.chat.completions.create(
            model=self.settings.llm_model,
            messages=conversation,
            temperature=self.settings.llm_temperature,
            max_tokens=self.settings.max_tokens
        )
        
        result["response"] = final_response.choices[0].message.content
        
        return result
    
    def _execute_search_kb(self, args: dict) -> dict:
        """Execute the search_knowledge_base tool."""
        from tools.tool_definitions import execute_search_knowledge_base
        query = args.get("query", "")
        return execute_search_knowledge_base(query, self.rag_service)
    
    def _execute_book_demo(self, args: dict) -> dict:
        """Execute the book_demo tool."""
        from tools.tool_definitions import execute_book_demo
        return execute_book_demo(**args)


# Singleton instance
_llm_service_instance = None


def get_llm_service(rag_service) -> LLMService:
    """Get or create LLM service singleton."""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService(rag_service)
    return _llm_service_instance

