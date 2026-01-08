"""
Recommendation Agent for the Retail Order Query Chatbot.

Provides personalized product recommendations.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationAgent(BaseAgent):
    """
    Agent specialized in product recommendations.
    
    Capabilities:
    - Suggest similar products
    - Cross-sell related items
    - Upsell premium options
    - Personalize based on history
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="RecommendationAgent",
            description="Provides personalized product recommendations",
            temperature=0.5,
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get recommendation tools."""
        
        @tool("get_similar_products")
        def get_similar_tool(product_id: str) -> Dict[str, Any]:
            """
            Get products similar to a given product.
            
            Args:
                product_id: Product identifier
                
            Returns:
                List of similar products
            """
            return {
                "product_id": product_id,
                "similar_products": [
                    {"id": "PROD-002", "name": "Samsung Galaxy S24 Ultra", "price": 1199.00, "match_score": 0.92},
                    {"id": "PROD-003", "name": "Google Pixel 8 Pro", "price": 999.00, "match_score": 0.88},
                    {"id": "PROD-004", "name": "OnePlus 12", "price": 799.00, "match_score": 0.85},
                ]
            }
        
        @tool("get_personalized_recommendations")
        def get_personalized_tool(customer_id: str) -> Dict[str, Any]:
            """
            Get personalized recommendations for customer.
            
            Args:
                customer_id: Customer identifier
                
            Returns:
                Personalized product recommendations
            """
            return {
                "customer_id": customer_id,
                "recommendations": [
                    {
                        "id": "PROD-010",
                        "name": "AirPods Pro 2",
                        "price": 249.00,
                        "reason": "Based on your iPhone purchase"
                    },
                    {
                        "id": "PROD-011",
                        "name": "MagSafe Charger",
                        "price": 39.00,
                        "reason": "Popular with iPhone users"
                    },
                    {
                        "id": "PROD-012",
                        "name": "iPhone 15 Pro Case",
                        "price": 49.00,
                        "reason": "Protect your new phone"
                    }
                ],
                "based_on": ["purchase_history", "browsing_behavior", "similar_customers"]
            }
        
        @tool("get_cross_sell_items")
        def get_cross_sell_tool(cart_items: str) -> Dict[str, Any]:
            """
            Get cross-sell recommendations based on cart.
            
            Args:
                cart_items: Comma-separated product IDs in cart
                
            Returns:
                Cross-sell product suggestions
            """
            return {
                "cart_items": cart_items.split(","),
                "cross_sell": [
                    {
                        "id": "PROD-020",
                        "name": "AppleCare+ for iPhone",
                        "price": 199.00,
                        "savings": "Save 20% when bought with iPhone"
                    },
                    {
                        "id": "PROD-021",
                        "name": "Lightning to USB-C Cable",
                        "price": 19.00,
                        "reason": "Essential accessory"
                    }
                ]
            }
        
        @tool("get_trending_products")
        def get_trending_tool(category: str = "") -> Dict[str, Any]:
            """
            Get trending products.
            
            Args:
                category: Optional category filter
                
            Returns:
                Trending products
            """
            return {
                "category": category or "all",
                "trending": [
                    {"id": "PROD-001", "name": "iPhone 15 Pro", "sales_trend": "+45%", "rank": 1},
                    {"id": "PROD-030", "name": "PS5 Slim", "sales_trend": "+38%", "rank": 2},
                    {"id": "PROD-031", "name": "Stanley Tumbler", "sales_trend": "+120%", "rank": 3},
                ],
                "period": "last_7_days"
            }
        
        return [
            get_similar_tool,
            get_personalized_tool,
            get_cross_sell_tool,
            get_trending_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Recommendation Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Suggest similar products when customers are browsing
2. Provide personalized recommendations based on history
3. Cross-sell complementary items
4. Upsell premium alternatives
5. Highlight trending products

Recommendation Strategies:
- Similar Products: Items with similar features/category
- Personalized: Based on purchase/browsing history
- Cross-sell: Complementary accessories or add-ons
- Upsell: Higher-tier options with more features
- Trending: Popular items in the category

Response Guidelines:
- Explain WHY you're recommending each item
- Show price and value proposition
- Highlight any bundle deals or savings
- Limit to 3-5 recommendations
- Make it feel personalized, not pushy

Show products in an appealing, easy-to-compare format."""
    
    async def recommend(
        self,
        customer_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get recommendations for a customer."""
        logger.info(f"Getting recommendations for customer: {customer_id}")
        
        return {
            "customer_id": customer_id,
            "recommendations": [
                {"name": "AirPods Pro 2", "price": 249.00, "reason": "Perfect match for your iPhone"}
            ]
        }
