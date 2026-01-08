"""
Product Agent for the Retail Order Query Chatbot.

Handles product-related queries, searches, and information.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductAgent(BaseAgent):
    """
    Agent specialized in product queries.
    
    Capabilities:
    - Search products
    - Check availability/inventory
    - Compare products
    - Provide product details and specs
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ProductAgent",
            description="Handles product queries, searches, and information",
            temperature=0.3,
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get product-related tools."""
        
        @tool("search_products")
        def search_products_tool(
            query: str,
            category: str = "",
            max_price: float = 0,
            in_stock_only: bool = True
        ) -> Dict[str, Any]:
            """
            Search for products matching query.
            
            Args:
                query: Search query
                category: Product category filter
                max_price: Maximum price filter
                in_stock_only: Only show in-stock items
                
            Returns:
                List of matching products
            """
            # Mock product catalog
            products = [
                {
                    "id": "PROD-001",
                    "name": "iPhone 15 Pro - Blue Titanium",
                    "category": "Electronics",
                    "price": 999.00,
                    "variants": [
                        {"storage": "128GB", "price": 999.00, "stock": 15},
                        {"storage": "256GB", "price": 1099.00, "stock": 8},
                        {"storage": "512GB", "price": 1299.00, "stock": 2},
                        {"storage": "1TB", "price": 1499.00, "stock": 5},
                    ],
                    "in_stock": True,
                    "rating": 4.8,
                    "reviews": 1250
                },
                {
                    "id": "PROD-002",
                    "name": "Samsung Galaxy S24 Ultra",
                    "category": "Electronics",
                    "price": 1199.00,
                    "variants": [
                        {"storage": "256GB", "price": 1199.00, "stock": 20},
                        {"storage": "512GB", "price": 1399.00, "stock": 12},
                    ],
                    "in_stock": True,
                    "rating": 4.7,
                    "reviews": 890
                },
                {
                    "id": "PROD-003",
                    "name": "Nike Air Max 270 - Running Shoes",
                    "category": "Footwear",
                    "price": 150.00,
                    "sizes": [7, 8, 9, 10, 11, 12],
                    "colors": ["Black", "White", "Red"],
                    "in_stock": True,
                    "rating": 4.5,
                    "reviews": 2340
                },
            ]
            
            # Filter by query
            query_lower = query.lower()
            results = [p for p in products if query_lower in p["name"].lower()]
            
            # Filter by price
            if max_price > 0:
                results = [p for p in results if p["price"] <= max_price]
            
            return {
                "query": query,
                "products": results,
                "total_results": len(results)
            }
        
        @tool("get_product_details")
        def get_product_details_tool(product_id: str) -> Dict[str, Any]:
            """
            Get detailed information about a product.
            
            Args:
                product_id: Product identifier
                
            Returns:
                Product details
            """
            # Mock product details
            return {
                "id": product_id,
                "name": "iPhone 15 Pro - Blue Titanium",
                "description": "The most advanced iPhone ever with A17 Pro chip.",
                "category": "Electronics",
                "brand": "Apple",
                "price": 999.00,
                "specs": {
                    "display": "6.1-inch Super Retina XDR",
                    "chip": "A17 Pro",
                    "camera": "48MP main camera",
                    "battery": "Up to 29 hours video playback"
                },
                "variants": [
                    {"storage": "128GB", "price": 999.00},
                    {"storage": "256GB", "price": 1099.00},
                    {"storage": "512GB", "price": 1299.00},
                    {"storage": "1TB", "price": 1499.00},
                ],
                "colors": ["Blue Titanium", "Black Titanium", "White Titanium", "Natural Titanium"],
                "in_stock": True,
                "rating": 4.8,
                "reviews_count": 1250
            }
        
        @tool("check_inventory")
        def check_inventory_tool(
            product_id: str,
            variant: str = ""
        ) -> Dict[str, Any]:
            """
            Check product inventory/availability.
            
            Args:
                product_id: Product identifier
                variant: Specific variant (size, color, etc.)
                
            Returns:
                Inventory status
            """
            return {
                "product_id": product_id,
                "variant": variant,
                "in_stock": True,
                "quantity": 15,
                "low_stock_threshold": 5,
                "is_low_stock": False,
                "restock_date": None,
                "stores_with_stock": ["Main Warehouse", "Store NYC", "Store LA"]
            }
        
        @tool("compare_products")
        def compare_products_tool(product_ids: str) -> Dict[str, Any]:
            """
            Compare multiple products.
            
            Args:
                product_ids: Comma-separated product IDs
                
            Returns:
                Comparison data
            """
            ids = product_ids.split(",")
            
            comparison = {
                "products": [
                    {"id": "PROD-001", "name": "iPhone 15 Pro", "price": 999, "rating": 4.8},
                    {"id": "PROD-002", "name": "Samsung Galaxy S24", "price": 1199, "rating": 4.7},
                ],
                "comparison_attributes": {
                    "display": {"PROD-001": "6.1 inch", "PROD-002": "6.8 inch"},
                    "camera": {"PROD-001": "48MP", "PROD-002": "200MP"},
                    "battery": {"PROD-001": "3274 mAh", "PROD-002": "5000 mAh"},
                }
            }
            
            return comparison
        
        return [
            search_products_tool,
            get_product_details_tool,
            check_inventory_tool,
            compare_products_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Product Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Search for products based on customer queries
2. Provide detailed product information
3. Check product availability and inventory
4. Compare products when requested
5. Help customers find what they're looking for

Product Information to Include:
- Name and description
- Price and variants (sizes, colors, storage)
- Availability status
- Key specifications
- Ratings and reviews summary

Response Guidelines:
- Be helpful and informative
- Use emojis for visual appeal (📱, ✅, ⚠️, 💰)
- Format prices clearly
- Highlight stock status
- Suggest alternatives if out of stock

Always provide clear, structured product information."""
    
    async def search(self, query: str) -> Dict[str, Any]:
        """Search for products."""
        logger.info(f"Searching products: {query}")
        
        # Mock search results
        results = [
            {
                "id": "PROD-001",
                "name": f"iPhone 15 Pro - Blue Titanium",
                "price": 999.00,
                "in_stock": True,
                "rating": 4.8
            }
        ]
        
        return {"query": query, "products": results}
