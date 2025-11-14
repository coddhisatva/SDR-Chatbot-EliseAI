"""
OpenAI Function/Tool Definitions
Defines the tools available to the AI SDR.
"""

from config import get_settings


def get_tool_definitions() -> list[dict]:
    """
    Get the list of tool definitions for OpenAI function calling.
    
    Returns:
        List of tool definition dicts in OpenAI format
    """
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": (
                    "Search EliseAI's blog articles for detailed information about products, "
                    "features, case studies, pricing, implementation details, or industry insights. "
                    "Use this when you need specific facts, examples, statistics, or detailed explanations "
                    "beyond your basic product knowledge. Do NOT use for basic greetings, qualification "
                    "questions, or simple product overviews."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "The search query. Be specific about what information you need. "
                                "Examples: 'LeasingAI features and benefits', 'case studies for property management', "
                                "'DelinquencyAI pricing and ROI', 'MaintenanceAI implementation process'"
                            )
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "book_demo",
                "description": (
                    "Provide a Calendly demo booking link when the prospect expresses interest in scheduling a demo, "
                    "learning more, or taking next steps. Use this when they say things like 'I want to book a demo', "
                    "'I'm ready to buy', 'Let's schedule a call', 'How do we get started?', etc. "
                    "Do NOT ask for their information manually - Calendly will collect it. "
                    "Just provide the link so they can self-schedule."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Brief note on why they want a demo (e.g., 'interested in LeasingAI', 'ready to buy')"
                        }
                    },
                    "required": []
                }
            }
        }
    ]
    
    return tools


def execute_search_knowledge_base(query: str, rag_service) -> dict:
    """
    Execute the search_knowledge_base tool.
    
    Args:
        query: Search query string
        rag_service: RAGService instance
    
    Returns:
        Dict with search results and formatted content
    """
    results = rag_service.search(query)
    formatted_content = rag_service.format_results_for_llm(results)
    citations = rag_service.get_source_citations(results)
    
    return {
        "results": results,
        "formatted_content": formatted_content,
        "citations": citations
    }


def execute_book_demo(reason: str = None) -> dict:
    """
    Execute the book_demo tool.
    
    Args:
        reason: Brief note on why they want a demo (optional)
    
    Returns:
        Dict with calendly link and confirmation message
    """
    settings = get_settings()
    
    return {
        "calendly_url": settings.calendly_demo_link,
        "message": (
            "Perfect! I've prepared your demo booking link below. "
            "Click it to choose a time that works best for you. "
            "You'll be able to provide your details and select a time slot directly through Calendly."
        )
    }

