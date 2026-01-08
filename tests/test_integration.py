"""
Integration tests for the Retail Order Query Chatbot API.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from src.api.routes import app
    return TestClient(app)


class TestAPIRoot:
    """Test API root endpoints."""
    
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "Retail" in data["name"]
    
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestChatAPI:
    """Test chat endpoints."""
    
    def test_chat_product_query(self, client):
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Do you have iPhone 15 Pro?",
                "customer_id": "TEST-001"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "session_id" in data
    
    def test_chat_order_tracking(self, client):
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Where is my order #12345?",
                "customer_id": "TEST-001"
            }
        )
        assert response.status_code == 200


class TestProductAPI:
    """Test product endpoints."""
    
    def test_search_products(self, client):
        response = client.post(
            "/api/v1/products/search",
            json={
                "query": "iPhone",
                "in_stock_only": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
    
    def test_get_product_details(self, client):
        response = client.get("/api/v1/products/PROD-001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "PROD-001"


class TestOrderAPI:
    """Test order endpoints."""
    
    def test_track_order(self, client):
        response = client.post(
            "/api/v1/orders/track",
            json={"order_id": "ORD-12345"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == "ORD-12345"
        assert "status" in data
    
    def test_get_order_details(self, client):
        response = client.get("/api/v1/orders/ORD-12345")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data


class TestCartAPI:
    """Test cart endpoints."""
    
    def test_get_cart(self, client):
        response = client.get("/api/v1/cart/CUST-001")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_apply_valid_coupon(self, client):
        response = client.post(
            "/api/v1/cart/coupon",
            json={
                "cart_id": "CART-001",
                "coupon_code": "SAVE10"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
    
    def test_apply_invalid_coupon(self, client):
        response = client.post(
            "/api/v1/cart/coupon",
            json={
                "cart_id": "CART-001",
                "coupon_code": "INVALID"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False


class TestReturnAPI:
    """Test return endpoints."""
    
    def test_create_return(self, client):
        response = client.post(
            "/api/v1/returns",
            json={
                "order_id": "ORD-12345",
                "reason": "Changed my mind"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "return_id" in data
        assert data["status"] == "initiated"
    
    def test_get_return_status(self, client):
        response = client.get("/api/v1/returns/RET-12345")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestRecommendationsAPI:
    """Test recommendations endpoints."""
    
    def test_get_recommendations(self, client):
        response = client.get("/api/v1/recommendations/CUST-001")
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
