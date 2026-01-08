"""
Router Agent for the Retail Order Query Chatbot.

Classifies customer intent and routes to appropriate specialized agent.
"""

from typing import Any, Dict, List, Optional
from enum import Enum

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent, AgentResult
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CustomerIntent(str, Enum):
    """Possible customer intents."""
    PRODUCT_QUERY = "product_query"
    ORDER_STATUS = "order_status"
    RECOMMENDATION = "recommendation"
    RETURN_REQUEST = "return_request"
    CART_HELP = "cart_help"
    CHECKOUT_HELP = "checkout_help"
    GENERAL_INQUIRY = "general_inquiry"


class RouterAgent(BaseAgent):
    """
    Agent that classifies customer intent and routes to appropriate agent.
    
    Responsibilities:
    - Analyze customer message
    - Classify intent
    - Extract key entities
    - Route to specialized agent
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="RouterAgent",
            description="Classifies customer intent and routes queries",
            temperature=0.2,  # Low temperature for consistent classification
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get routing tools."""
        
        @tool("classify_intent")
        def classify_intent_tool(message: str) -> Dict[str, Any]:
            """
            Classify the customer's intent from their message.
            
            Args:
                message: Customer message
                
            Returns:
                Intent classification result
            """
            message_lower = message.lower()
            
            # Order-related keywords
            if any(kw in message_lower for kw in ["order", "track", "where is", "delivery", "shipping", "arrived"]):
                intent = CustomerIntent.ORDER_STATUS
            # Return/refund keywords
            elif any(kw in message_lower for kw in ["return", "refund", "exchange", "broken", "damaged", "wrong"]):
                intent = CustomerIntent.RETURN_REQUEST
            # Cart/checkout keywords
            elif any(kw in message_lower for kw in ["cart", "checkout", "pay", "coupon", "discount", "promo"]):
                intent = CustomerIntent.CART_HELP
            # Recommendation keywords
            elif any(kw in message_lower for kw in ["recommend", "suggest", "similar", "like this", "alternative"]):
                intent = CustomerIntent.RECOMMENDATION
            # Product query (default for product-related)
            elif any(kw in message_lower for kw in ["have", "stock", "available", "price", "specs", "feature", "size", "color"]):
                intent = CustomerIntent.PRODUCT_QUERY
            else:
                intent = CustomerIntent.GENERAL_INQUIRY
            
            return {
                "intent": intent.value,
                "confidence": 0.85,
                "message": message
            }
        
        @tool("extract_entities")
        def extract_entities_tool(message: str) -> Dict[str, Any]:
            """
            Extract key entities from customer message.
            
            Args:
                message: Customer message
                
            Returns:
                Extracted entities
            """
            entities = {
                "order_id": None,
                "product_name": None,
                "product_id": None,
                "size": None,
                "color": None,
                "quantity": None,
            }
            
            # Simple entity extraction
            message_lower = message.lower()
            
            # Order ID pattern
            if "#" in message:
                import re
                order_match = re.search(r'#(\d+)', message)
                if order_match:
                    entities["order_id"] = order_match.group(1)
            
            # Color extraction
            colors = ["red", "blue", "green", "black", "white", "pink", "gold", "silver"]
            for color in colors:
                if color in message_lower:
                    entities["color"] = color
                    break
            
            # Size extraction
            sizes = ["small", "medium", "large", "xl", "xxl", "xs"]
            for size in sizes:
                if size in message_lower:
                    entities["size"] = size
                    break
            
            return entities
        
        @tool("get_routing_decision")
        def get_routing_decision_tool(
            intent: str,
            entities: str
        ) -> Dict[str, Any]:
            """
            Determine which agent should handle the request.
            
            Args:
                intent: Classified intent
                entities: Extracted entities as JSON string
                
            Returns:
                Routing decision
            """
            routing_map = {
                "product_query": "ProductAgent",
                "order_status": "OrderAgent",
                "recommendation": "RecommendationAgent",
                "return_request": "SupportAgent",
                "cart_help": "CheckoutAgent",
                "checkout_help": "CheckoutAgent",
                "general_inquiry": "ProductAgent",  # Default to product
            }
            
            return {
                "target_agent": routing_map.get(intent, "ProductAgent"),
                "intent": intent,
                "priority": "normal"
            }
        
        return [
            classify_intent_tool,
            extract_entities_tool,
            get_routing_decision_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Router Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Analyze the customer's message
2. Classify their intent accurately
3. Extract relevant entities (order IDs, product names, colors, sizes)
4. Route to the appropriate specialized agent

Available Intents:
- product_query: Questions about products, availability, specs, pricing
- order_status: Order tracking, delivery updates, shipping questions
- recommendation: Product suggestions, alternatives, similar items
- return_request: Returns, refunds, exchanges, complaints
- cart_help: Cart management, checkout, payment, coupons

Routing Rules:
- Be precise in classification
- If unclear, default to product_query
- Extract as many entities as possible
- Note urgency level if applicable

Always provide structured output with intent and entities."""
    
    async def route(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Route a customer message to the appropriate agent.
        
        Args:
            message: Customer message
            context: Conversation context
            
        Returns:
            Routing decision with intent and target agent
        """
        logger.info(f"Routing message: {message[:50]}...")
        
        # Simple intent classification
        message_lower = message.lower()
        
        if any(kw in message_lower for kw in ["order", "track", "where is", "delivery"]):
            intent = CustomerIntent.ORDER_STATUS
            target = "OrderAgent"
        elif any(kw in message_lower for kw in ["return", "refund", "exchange"]):
            intent = CustomerIntent.RETURN_REQUEST
            target = "SupportAgent"
        elif any(kw in message_lower for kw in ["cart", "checkout", "coupon"]):
            intent = CustomerIntent.CART_HELP
            target = "CheckoutAgent"
        elif any(kw in message_lower for kw in ["recommend", "suggest", "similar"]):
            intent = CustomerIntent.RECOMMENDATION
            target = "RecommendationAgent"
        else:
            intent = CustomerIntent.PRODUCT_QUERY
            target = "ProductAgent"
        
        return {
            "intent": intent.value,
            "target_agent": target,
            "message": message,
            "context": context
        }
