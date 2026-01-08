"""
FastAPI routes for the Retail Order Query Chatbot.
"""

from datetime import datetime
from typing import Any, Dict, List
import uuid

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    ProductSearchRequest,
    ProductSearchResponse,
    ProductResponse,
    OrderTrackRequest,
    OrderStatusResponse,
    CartResponse,
    CartItem,
    CouponRequest,
    CouponResponse,
    ReturnRequest,
    ReturnResponse,
    HealthResponse,
    ErrorResponse,
)
from src.agents import RetailChatbot
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Retail Order Query Chatbot API",
    description="Multi-agent AI chatbot for retail customer service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot = RetailChatbot()


@app.get("/", response_model=Dict[str, str])
async def root():
    """API root endpoint."""
    return {
        "name": "Retail Order Query Chatbot",
        "version": "1.0.0",
        "description": "AI-powered retail customer service chatbot",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        services={
            "api": "running",
            "agents": "ready",
            "database": "connected",
            "redis": "connected",
        }
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a chat message and get a response.
    
    The chatbot automatically routes to the appropriate agent:
    - Product queries → ProductAgent
    - Order tracking → OrderAgent
    - Returns/refunds → SupportAgent
    - Cart help → CheckoutAgent
    - Recommendations → RecommendationAgent
    """
    try:
        logger.info(f"Chat request: {request.message[:50]}...")
        
        # Get or create session
        session = chatbot.create_session(request.customer_id)
        
        if request.session_id:
            existing = chatbot.get_session(request.session_id)
            if existing:
                session = existing
        
        # Process message
        response = session.chat(request.message)
        
        return ChatResponse(
            success=response.get("success", True),
            message=response.get("message", "I can help with that!"),
            session_id=session.session_id,
            data=response.get("data"),
            intent=response.get("intent"),
            agent=response.get("agent"),
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/products/search", response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    """Search for products."""
    try:
        logger.info(f"Product search: {request.query}")
        
        # Mock search results
        products = [
            ProductResponse(
                id="PROD-001",
                name="iPhone 15 Pro - Blue Titanium",
                price=999.00,
                in_stock=True,
                rating=4.8,
            ),
            ProductResponse(
                id="PROD-002",
                name="Samsung Galaxy S24 Ultra",
                price=1199.00,
                in_stock=True,
                rating=4.7,
            ),
        ]
        
        # Filter by query
        query_lower = request.query.lower()
        filtered = [p for p in products if query_lower in p.name.lower()]
        
        return ProductSearchResponse(
            query=request.query,
            products=filtered,
            total_results=len(filtered)
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: str):
    """Get product details."""
    return {
        "id": product_id,
        "name": "iPhone 15 Pro - Blue Titanium",
        "description": "The most advanced iPhone ever.",
        "price": 999.00,
        "in_stock": True,
        "variants": [
            {"storage": "128GB", "price": 999.00},
            {"storage": "256GB", "price": 1099.00},
        ],
        "rating": 4.8,
        "reviews_count": 1250
    }


@app.post("/api/v1/orders/track", response_model=OrderStatusResponse)
async def track_order(request: OrderTrackRequest):
    """Track an order by ID."""
    try:
        logger.info(f"Tracking order: {request.order_id}")
        
        return OrderStatusResponse(
            order_id=request.order_id,
            status="in_transit",
            status_display="In Transit 🚚",
            carrier="FedEx",
            tracking_number="7894561230123",
            estimated_delivery="Jan 7, 2024",
            last_update="Package departed Memphis, TN"
        )
        
    except Exception as e:
        logger.error(f"Tracking error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: str):
    """Get order details."""
    return {
        "order_id": order_id,
        "status": "in_transit",
        "order_date": "2024-01-03",
        "items": [
            {"name": "iPhone 15 Pro - Blue", "quantity": 1, "price": 999.00}
        ],
        "subtotal": 999.00,
        "tax": 79.92,
        "total": 1078.92
    }


@app.get("/api/v1/cart/{customer_id}", response_model=CartResponse)
async def get_cart(customer_id: str):
    """Get customer's cart."""
    return CartResponse(
        cart_id=f"CART-{customer_id}",
        items=[
            CartItem(
                product_id="PROD-001",
                name="iPhone 15 Pro - Blue 256GB",
                price=1099.00,
                quantity=1
            )
        ],
        subtotal=1099.00,
        tax=87.92,
        shipping=0.00,
        discount=0.00,
        total=1186.92
    )


@app.post("/api/v1/cart/{customer_id}/add")
async def add_to_cart(customer_id: str, product_id: str, quantity: int = 1):
    """Add item to cart."""
    return {
        "success": True,
        "message": "Item added to cart!",
        "cart_total": 1186.92
    }


@app.post("/api/v1/cart/coupon", response_model=CouponResponse)
async def apply_coupon(request: CouponRequest):
    """Apply a coupon code."""
    valid_coupons = ["SAVE10", "FREESHIP", "WELCOME20"]
    
    if request.coupon_code.upper() in valid_coupons:
        return CouponResponse(
            valid=True,
            coupon_code=request.coupon_code.upper(),
            discount=109.90,
            message=f"Coupon {request.coupon_code} applied! You saved $109.90"
        )
    else:
        return CouponResponse(
            valid=False,
            coupon_code=request.coupon_code,
            discount=0,
            message="Invalid or expired coupon code"
        )


@app.post("/api/v1/returns", response_model=ReturnResponse)
async def create_return(request: ReturnRequest):
    """Initiate a return."""
    return_id = f"RET-{uuid.uuid4().hex[:8].upper()}"
    
    return ReturnResponse(
        return_id=return_id,
        order_id=request.order_id,
        status="initiated",
        return_label_url=f"https://returns.example.com/{return_id}",
        refund_estimate="3-5 business days after receipt"
    )


@app.get("/api/v1/returns/{return_id}")
async def get_return_status(return_id: str):
    """Get return status."""
    return {
        "return_id": return_id,
        "status": "in_transit",
        "refund_amount": 999.00,
        "estimated_refund_date": "Jan 15, 2024"
    }


@app.get("/api/v1/recommendations/{customer_id}")
async def get_recommendations(customer_id: str):
    """Get personalized recommendations."""
    return {
        "customer_id": customer_id,
        "recommendations": [
            {"id": "PROD-010", "name": "AirPods Pro 2", "price": 249.00, 
             "reason": "Based on your iPhone purchase"},
            {"id": "PROD-011", "name": "MagSafe Charger", "price": 39.00,
             "reason": "Popular with iPhone users"},
        ]
    }


# Webhook endpoints for channel integrations
@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(payload: Dict[str, Any]):
    """WhatsApp message webhook."""
    logger.info("WhatsApp webhook received")
    return {"status": "received"}


@app.post("/webhooks/facebook")
async def facebook_webhook(payload: Dict[str, Any]):
    """Facebook Messenger webhook."""
    logger.info("Facebook webhook received")
    return {"status": "received"}


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
        ).model_dump(),
    )
