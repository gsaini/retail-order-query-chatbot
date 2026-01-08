"""
API request/response schemas for the Retail Order Query Chatbot.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat message request."""
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    customer_id: str = Field(default="anonymous")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Do you have the iPhone 15 Pro in blue?",
                "customer_id": "CUST-12345"
            }
        }


class ChatResponse(BaseModel):
    """Chat response."""
    success: bool
    message: str
    session_id: str
    data: Optional[Dict[str, Any]] = None
    intent: Optional[str] = None
    agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ProductSearchRequest(BaseModel):
    """Product search request."""
    query: str = Field(..., min_length=1)
    category: Optional[str] = None
    max_price: Optional[float] = None
    in_stock_only: bool = True


class ProductResponse(BaseModel):
    """Product information."""
    id: str
    name: str
    price: float
    in_stock: bool
    rating: Optional[float] = None
    image_url: Optional[str] = None


class ProductSearchResponse(BaseModel):
    """Product search response."""
    query: str
    products: List[ProductResponse]
    total_results: int


class OrderTrackRequest(BaseModel):
    """Order tracking request."""
    order_id: str = Field(..., min_length=1)


class OrderStatusResponse(BaseModel):
    """Order status response."""
    order_id: str
    status: str
    status_display: str
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[str] = None
    last_update: Optional[str] = None


class CartItem(BaseModel):
    """Cart item."""
    product_id: str
    name: str
    price: float
    quantity: int


class CartResponse(BaseModel):
    """Cart response."""
    cart_id: str
    items: List[CartItem]
    subtotal: float
    tax: float
    shipping: float
    discount: float
    total: float


class CouponRequest(BaseModel):
    """Coupon application request."""
    cart_id: str
    coupon_code: str


class CouponResponse(BaseModel):
    """Coupon response."""
    valid: bool
    coupon_code: str
    discount: float
    message: str


class ReturnRequest(BaseModel):
    """Return request."""
    order_id: str
    reason: str
    items: str = "all"


class ReturnResponse(BaseModel):
    """Return response."""
    return_id: str
    order_id: str
    status: str
    return_label_url: Optional[str] = None
    refund_estimate: str


class HealthResponse(BaseModel):
    """API health check response."""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
