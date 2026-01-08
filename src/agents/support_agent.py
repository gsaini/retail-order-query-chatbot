"""
Support Agent for the Retail Order Query Chatbot.

Handles returns, refunds, and customer complaints.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import uuid

from langchain_core.tools import BaseTool, tool

from src.agents.base import BaseAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SupportAgent(BaseAgent):
    """
    Agent specialized in customer support.
    
    Capabilities:
    - Process return requests
    - Handle refund inquiries
    - Manage exchanges
    - Escalate complaints
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="SupportAgent",
            description="Handles returns, refunds, and customer complaints",
            temperature=0.3,
            **kwargs
        )
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get support tools."""
        
        @tool("check_return_eligibility")
        def check_return_tool(order_id: str) -> Dict[str, Any]:
            """
            Check if an order is eligible for return.
            
            Args:
                order_id: Order identifier
                
            Returns:
                Return eligibility information
            """
            return {
                "order_id": order_id,
                "eligible": True,
                "return_window_days": 30,
                "days_remaining": 25,
                "return_type": ["full_refund", "exchange", "store_credit"],
                "items": [
                    {
                        "name": "iPhone 15 Pro - Blue",
                        "returnable": True,
                        "refund_amount": 999.00
                    }
                ],
                "return_conditions": [
                    "Item must be unused and in original packaging",
                    "All accessories must be included",
                    "Original receipt required"
                ]
            }
        
        @tool("initiate_return")
        def initiate_return_tool(
            order_id: str,
            reason: str,
            items: str = "all"
        ) -> Dict[str, Any]:
            """
            Initiate a return request.
            
            Args:
                order_id: Order identifier
                reason: Reason for return
                items: Items to return (all or comma-separated IDs)
                
            Returns:
                Return request confirmation
            """
            return_id = f"RET-{uuid.uuid4().hex[:8].upper()}"
            
            return {
                "return_id": return_id,
                "order_id": order_id,
                "status": "initiated",
                "reason": reason,
                "items": items,
                "return_label": "https://example.com/return-label/12345",
                "drop_off_locations": [
                    "Any FedEx location",
                    "Schedule pickup"
                ],
                "refund_estimate": {
                    "amount": 999.00,
                    "method": "original_payment",
                    "processing_days": "3-5 business days after receipt"
                }
            }
        
        @tool("get_return_status")
        def get_return_status_tool(return_id: str) -> Dict[str, Any]:
            """
            Get status of a return request.
            
            Args:
                return_id: Return identifier
                
            Returns:
                Return status information
            """
            return {
                "return_id": return_id,
                "status": "in_transit",
                "tracker": [
                    {"date": "2024-01-05", "status": "Return initiated"},
                    {"date": "2024-01-06", "status": "Package dropped off"},
                    {"date": "2024-01-07", "status": "In transit to warehouse"}
                ],
                "estimated_arrival": "2024-01-10",
                "refund_after_inspection": True
            }
        
        @tool("process_refund")
        def process_refund_tool(
            order_id: str,
            refund_type: str = "original_payment"
        ) -> Dict[str, Any]:
            """
            Process a refund for an order.
            
            Args:
                order_id: Order identifier
                refund_type: Type of refund (original_payment, store_credit)
                
            Returns:
                Refund confirmation
            """
            refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
            
            return {
                "refund_id": refund_id,
                "order_id": order_id,
                "status": "processing",
                "refund_amount": 999.00,
                "refund_method": refund_type,
                "estimated_processing": "3-5 business days",
                "confirmation_sent": True
            }
        
        @tool("create_support_ticket")
        def create_ticket_tool(
            issue_type: str,
            description: str,
            order_id: str = ""
        ) -> Dict[str, Any]:
            """
            Create a support ticket for complex issues.
            
            Args:
                issue_type: Type of issue
                description: Issue description
                order_id: Related order ID if applicable
                
            Returns:
                Ticket creation confirmation
            """
            ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            
            return {
                "ticket_id": ticket_id,
                "issue_type": issue_type,
                "priority": "normal",
                "status": "open",
                "estimated_response": "24-48 hours",
                "agent_assigned": False,
                "confirmation": f"We've received your request. Ticket #{ticket_id}"
            }
        
        return [
            check_return_tool,
            initiate_return_tool,
            get_return_status_tool,
            process_refund_tool,
            create_ticket_tool,
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are the Support Agent for a retail e-commerce chatbot.

Your responsibilities:
1. Handle return requests with empathy
2. Process refund inquiries
3. Manage product exchanges
4. Escalate complex issues
5. Ensure customer satisfaction

Return Policy Highlights:
- 30-day return window for most items
- Free return shipping
- Full refund to original payment method
- Exchanges available for different sizes/colors

Response Guidelines:
- Be empathetic and understanding
- Apologize for any inconvenience
- Explain the process clearly
- Provide return labels and instructions
- Set clear expectations on refund timing

Escalation Triggers:
- Damaged or defective products → Priority handling
- Repeated issues → Offer compensation
- Frustrated customers → Empathetic response + resolution

Always aim to resolve issues on first contact when possible."""
    
    async def process_return(
        self,
        order_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """Process a return request."""
        logger.info(f"Processing return for order: {order_id}")
        
        return_id = f"RET-{uuid.uuid4().hex[:8].upper()}"
        
        return {
            "return_id": return_id,
            "order_id": order_id,
            "status": "initiated",
            "return_label": "Provided",
            "refund_estimate": "3-5 business days"
        }
