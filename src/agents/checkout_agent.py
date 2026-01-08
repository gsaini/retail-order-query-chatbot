"""
Checkout Agent for the Retail Order Query Chatbot.

Assists with cart management and checkout process.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutAgent(BaseAgent):
    """
    Agent specialized in cart and checkout assistance.
    
    Capabilities:
    - Manage cart items
    - Apply coupons and discounts
    - Assist with checkout
    - Handle payment queries
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="CheckoutAgent",
            description="Assists with cart management and checkout process",
            temperature=0.3,
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get checkout tools."""
        
        @tool("get_cart")
        def get_cart_tool(customer_id: str) -> Dict[str, Any]:
            """
            Get customer's current cart.
            
            Args:
                customer_id: Customer identifier
                
            Returns:
                Cart contents
            """
            return {
                "customer_id": customer_id,
                "cart_id": "CART-12345",
                "items": [
                    {
                        "id": "PROD-001",
                        "name": "iPhone 15 Pro - Blue 256GB",
                        "price": 1099.00,
                        "quantity": 1,
                        "image": "iphone15pro.jpg"
                    }
                ],
                "subtotal": 1099.00,
                "tax": 87.92,
                "shipping": 0.00,
                "discount": 0.00,
                "total": 1186.92,
                "items_count": 1
            }
        
        @tool("add_to_cart")
        def add_to_cart_tool(
            customer_id: str,
            product_id: str,
            quantity: int = 1
        ) -> Dict[str, Any]:
            """
            Add item to cart.
            
            Args:
                customer_id: Customer identifier
                product_id: Product to add
                quantity: Quantity to add
                
            Returns:
                Updated cart
            """
            return {
                "success": True,
                "product_id": product_id,
                "quantity": quantity,
                "cart_total": 1186.92,
                "items_count": 1,
                "message": "Item added to cart!"
            }
        
        @tool("apply_coupon")
        def apply_coupon_tool(
            cart_id: str,
            coupon_code: str
        ) -> Dict[str, Any]:
            """
            Apply a coupon code to cart.
            
            Args:
                cart_id: Cart identifier
                coupon_code: Coupon code to apply
                
            Returns:
                Coupon application result
            """
            # Mock coupon validation
            valid_coupons = {
                "SAVE10": {"type": "percentage", "value": 10, "min_order": 50},
                "FREESHIP": {"type": "free_shipping", "value": 0, "min_order": 0},
                "WELCOME20": {"type": "fixed", "value": 20, "min_order": 100},
            }
            
            coupon = valid_coupons.get(coupon_code.upper())
            
            if coupon:
                return {
                    "valid": True,
                    "coupon_code": coupon_code.upper(),
                    "discount_type": coupon["type"],
                    "discount_value": coupon["value"],
                    "savings": 109.90 if coupon["type"] == "percentage" else coupon["value"],
                    "new_total": 1077.02,
                    "message": f"Coupon {coupon_code} applied! You saved $109.90"
                }
            else:
                return {
                    "valid": False,
                    "coupon_code": coupon_code,
                    "message": "Sorry, this coupon code is invalid or expired."
                }
        
        @tool("update_cart_item")
        def update_cart_item_tool(
            cart_id: str,
            product_id: str,
            quantity: int
        ) -> Dict[str, Any]:
            """
            Update quantity of item in cart.
            
            Args:
                cart_id: Cart identifier
                product_id: Product to update
                quantity: New quantity (0 to remove)
                
            Returns:
                Updated cart status
            """
            if quantity == 0:
                return {
                    "success": True,
                    "action": "removed",
                    "product_id": product_id,
                    "message": "Item removed from cart"
                }
            
            return {
                "success": True,
                "action": "updated",
                "product_id": product_id,
                "new_quantity": quantity,
                "message": f"Quantity updated to {quantity}"
            }
        
        @tool("get_shipping_options")
        def get_shipping_tool(
            cart_id: str,
            zip_code: str
        ) -> Dict[str, Any]:
            """
            Get available shipping options.
            
            Args:
                cart_id: Cart identifier
                zip_code: Delivery zip code
                
            Returns:
                Available shipping options
            """
            return {
                "cart_id": cart_id,
                "zip_code": zip_code,
                "options": [
                    {
                        "method": "standard",
                        "name": "Standard Shipping",
                        "price": 0.00,
                        "estimated_days": "5-7 business days",
                        "free_above": 50.00
                    },
                    {
                        "method": "express",
                        "name": "Express Shipping",
                        "price": 14.99,
                        "estimated_days": "2-3 business days"
                    },
                    {
                        "method": "overnight",
                        "name": "Overnight Shipping",
                        "price": 29.99,
                        "estimated_days": "1 business day"
                    }
                ]
            }
        
        @tool("initiate_checkout")
        def initiate_checkout_tool(cart_id: str) -> Dict[str, Any]:
            """
            Begin checkout process.
            
            Args:
                cart_id: Cart identifier
                
            Returns:
                Checkout session info
            """
            checkout_id = f"CHK-{uuid.uuid4().hex[:8].upper()}"
            
            return {
                "checkout_id": checkout_id,
                "cart_id": cart_id,
                "status": "pending",
                "checkout_url": f"https://store.com/checkout/{checkout_id}",
                "expires_in_minutes": 30,
                "steps_remaining": ["shipping_address", "payment_method", "review"]
            }
        
        return [
            get_cart_tool,
            add_to_cart_tool,
            apply_coupon_tool,
            update_cart_item_tool,
            get_shipping_tool,
            initiate_checkout_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Checkout Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Help customers manage their cart
2. Apply coupons and discount codes
3. Explain shipping options
4. Assist with checkout process
5. Answer payment-related questions

Cart Assistance:
- Add/remove items
- Update quantities
- Show cart summary
- Calculate totals

Coupon Handling:
- Validate coupon codes
- Apply discounts
- Explain savings
- Suggest available promotions

Checkout Help:
- Guide through steps
- Explain shipping options
- Address payment concerns
- Handle errors gracefully

Response Guidelines:
- Show clear pricing breakdown
- Highlight any savings
- Make checkout feel easy
- Offer assistance proactively

Always reassure customers about secure checkout and return policies."""
    
    async def get_cart(self, customer_id: str) -> Dict[str, Any]:
        """Get customer cart."""
        logger.info(f"Getting cart for customer: {customer_id}")
        
        return {
            "customer_id": customer_id,
            "items": [{"name": "iPhone 15 Pro", "price": 1099.00}],
            "total": 1186.92
        }
