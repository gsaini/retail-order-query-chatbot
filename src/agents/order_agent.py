"""
Order Agent for the Retail Order Query Chatbot.

Handles order tracking, status inquiries, and shipping updates.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import uuid

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OrderAgent(BaseAgent):
    """
    Agent specialized in order management.
    
    Capabilities:
    - Track order status
    - Provide shipping updates
    - Estimate delivery dates
    - Handle order inquiries
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="OrderAgent",
            description="Handles order tracking and status inquiries",
            temperature=0.2,
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get order-related tools."""
        
        @tool("track_order")
        def track_order_tool(order_id: str) -> Dict[str, Any]:
            """
            Track an order by order ID.
            
            Args:
                order_id: Order identifier
                
            Returns:
                Order tracking information
            """
            # Mock order data
            return {
                "order_id": order_id,
                "status": "in_transit",
                "status_display": "In Transit 🚚",
                "ordered_date": "2024-01-03",
                "shipped_date": "2024-01-04",
                "carrier": "FedEx",
                "tracking_number": "7894561230123",
                "estimated_delivery": "2024-01-07",
                "latest_update": {
                    "timestamp": "2024-01-05 14:30",
                    "location": "Memphis, TN",
                    "status": "Package departed - On the way to destination"
                },
                "tracking_history": [
                    {"date": "2024-01-04", "status": "Shipped", "location": "Warehouse"},
                    {"date": "2024-01-04", "status": "In Transit", "location": "Chicago, IL"},
                    {"date": "2024-01-05", "status": "In Transit", "location": "Memphis, TN"},
                ],
                "items": [
                    {"name": "iPhone 15 Pro - Blue", "quantity": 1, "price": 999.00}
                ]
            }
        
        @tool("get_order_details")
        def get_order_details_tool(order_id: str) -> Dict[str, Any]:
            """
            Get complete order details.
            
            Args:
                order_id: Order identifier
                
            Returns:
                Complete order information
            """
            return {
                "order_id": order_id,
                "customer_id": "CUST-12345",
                "status": "processing",
                "order_date": "2024-01-03",
                "items": [
                    {"name": "iPhone 15 Pro - Blue", "sku": "IPH15P-BL-256", 
                     "quantity": 1, "price": 1099.00}
                ],
                "subtotal": 1099.00,
                "tax": 87.92,
                "shipping": 0.00,
                "total": 1186.92,
                "shipping_address": {
                    "name": "John Doe",
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001"
                },
                "payment_method": "Visa ending in 4242"
            }
        
        @tool("get_customer_orders")
        def get_customer_orders_tool(customer_id: str) -> Dict[str, Any]:
            """
            Get all orders for a customer.
            
            Args:
                customer_id: Customer identifier
                
            Returns:
                List of customer orders
            """
            return {
                "customer_id": customer_id,
                "orders": [
                    {
                        "order_id": "ORD-12345",
                        "date": "2024-01-03",
                        "status": "in_transit",
                        "total": 1186.92,
                        "items_count": 1
                    },
                    {
                        "order_id": "ORD-12344",
                        "date": "2023-12-20",
                        "status": "delivered",
                        "total": 299.99,
                        "items_count": 2
                    }
                ],
                "total_orders": 2
            }
        
        @tool("estimate_delivery")
        def estimate_delivery_tool(order_id: str) -> Dict[str, Any]:
            """
            Get estimated delivery date.
            
            Args:
                order_id: Order identifier
                
            Returns:
                Delivery estimate
            """
            estimated = datetime.now() + timedelta(days=3)
            
            return {
                "order_id": order_id,
                "estimated_delivery": estimated.strftime("%Y-%m-%d"),
                "delivery_window": "9:00 AM - 5:00 PM",
                "carrier": "FedEx",
                "delivery_type": "Standard",
                "can_expedite": True,
                "expedite_cost": 15.00
            }
        
        @tool("request_delivery_update")
        def request_update_tool(
            order_id: str,
            notification_type: str = "email"
        ) -> Dict[str, Any]:
            """
            Request delivery notifications.
            
            Args:
                order_id: Order identifier
                notification_type: Type of notification (email, sms, both)
                
            Returns:
                Notification status
            """
            return {
                "order_id": order_id,
                "notification_type": notification_type,
                "subscribed": True,
                "events": ["out_for_delivery", "delivered", "exception"]
            }
        
        return [
            track_order_tool,
            get_order_details_tool,
            get_customer_orders_tool,
            estimate_delivery_tool,
            request_update_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Order Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Track order status and provide updates
2. Show shipping information and carrier details
3. Estimate delivery dates
4. Answer order-related questions
5. Set up delivery notifications

Order Status Types:
- pending: Order received, awaiting processing
- processing: Being prepared for shipment
- shipped: Package with carrier
- in_transit: On the way to destination
- out_for_delivery: Arriving today
- delivered: Successfully delivered
- exception: Delivery issue

Response Format Guidelines:
- Use clear status indicators: ✅ 🚚 📦 📍
- Show timeline of tracking events
- Include carrier and tracking number
- Provide estimated delivery prominently
- Offer to set up notifications

Be proactive in offering delivery update notifications."""
    
    async def track(self, order_id: str) -> Dict[str, Any]:
        """Track an order."""
        logger.info(f"Tracking order: {order_id}")
        
        return {
            "order_id": order_id,
            "status": "in_transit",
            "carrier": "FedEx",
            "estimated_delivery": "Jan 7, 2024",
            "last_update": "Package departed Memphis, TN"
        }
