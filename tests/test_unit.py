"""
Unit tests for the Retail Order Query Chatbot.
"""

import pytest
from datetime import datetime


class TestValidators:
    """Tests for validation utilities."""
    
    def test_validate_email_valid(self):
        from src.utils.validators import validate_email
        
        valid, error = validate_email("test@example.com")
        assert valid is True
        
        valid, error = validate_email("user.name@domain.co.uk")
        assert valid is True
    
    def test_validate_email_invalid(self):
        from src.utils.validators import validate_email
        
        valid, error = validate_email("notanemail")
        assert valid is False
        
        valid, error = validate_email("")
        assert valid is False
    
    def test_validate_order_id_valid(self):
        from src.utils.validators import validate_order_id
        
        valid, error = validate_order_id("ORD-12345")
        assert valid is True
        
        valid, error = validate_order_id("#12345")
        assert valid is True
        
        valid, error = validate_order_id("12345678")
        assert valid is True
    
    def test_validate_order_id_invalid(self):
        from src.utils.validators import validate_order_id
        
        valid, error = validate_order_id("")
        assert valid is False
    
    def test_validate_coupon_code(self):
        from src.utils.validators import validate_coupon_code
        
        valid, error = validate_coupon_code("SAVE10")
        assert valid is True
        
        valid, error = validate_coupon_code("AB")
        assert valid is False
    
    def test_validate_phone(self):
        from src.utils.validators import validate_phone
        
        valid, error = validate_phone("1234567890")
        assert valid is True
        
        valid, error = validate_phone("123")
        assert valid is False
    
    def test_sanitize_search_query(self):
        from src.utils.validators import sanitize_search_query
        
        result = sanitize_search_query("iPhone <script>")
        assert "<" not in result
        assert ">" not in result


class TestFormatters:
    """Tests for formatting utilities."""
    
    def test_format_price(self):
        from src.utils.formatters import format_price
        
        assert format_price(99.99) == "$99.99"
        assert format_price(1234.56) == "$1,234.56"
        assert format_price(100, "EUR") == "€100.00"
    
    def test_format_date(self):
        from src.utils.formatters import format_date
        
        assert format_date("2024-01-15", "short") == "01/15/24"
        assert format_date("2024-01-15", "medium") == "Jan 15, 2024"
    
    def test_format_order_status(self):
        from src.utils.formatters import format_order_status
        
        assert "🚚" in format_order_status("in_transit")
        assert "✅" in format_order_status("delivered")
    
    def test_format_stock_status(self):
        from src.utils.formatters import format_stock_status
        
        assert "Out of Stock" in format_stock_status(0)
        assert "Low Stock" in format_stock_status(2)
        assert "In Stock" in format_stock_status(50)


class TestRouterAgent:
    """Tests for router agent."""
    
    def test_route_product_query(self):
        from src.agents.router_agent import RouterAgent
        import asyncio
        
        agent = RouterAgent()
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            agent.route("Do you have iPhone 15 in blue?")
        )
        
        assert result["target_agent"] == "ProductAgent"
        assert result["intent"] == "product_query"
    
    def test_route_order_tracking(self):
        from src.agents.router_agent import RouterAgent
        import asyncio
        
        agent = RouterAgent()
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            agent.route("Where is my order #12345?")
        )
        
        assert result["target_agent"] == "OrderAgent"
        assert result["intent"] == "order_status"
    
    def test_route_return_request(self):
        from src.agents.router_agent import RouterAgent
        import asyncio
        
        agent = RouterAgent()
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            agent.route("I want to return my purchase")
        )
        
        assert result["target_agent"] == "SupportAgent"
        assert result["intent"] == "return_request"


class TestProductAgent:
    """Tests for product agent."""
    
    def test_search_products(self):
        from src.agents.product_agent import ProductAgent
        import asyncio
        
        agent = ProductAgent()
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(agent.search("iPhone"))
        
        assert "products" in result
        assert "query" in result


class TestContextManager:
    """Tests for context manager."""
    
    def test_context_set_get(self):
        from src.context.context_manager import ContextManager
        
        ctx = ContextManager("test-session")
        
        ctx.set("customer_id", "CUST-123")
        assert ctx.get("customer_id") == "CUST-123"
        assert ctx.get("nonexistent") is None
    
    def test_context_message_history(self):
        from src.context.context_manager import ContextManager
        
        ctx = ContextManager("test-session")
        
        ctx.add_message("user", "Hello")
        ctx.add_message("assistant", "Hi there!")
        
        history = ctx.get_history()
        assert len(history) == 2
        assert history[0]["role"] == "user"
    
    def test_context_reset(self):
        from src.context.context_manager import ContextManager
        
        ctx = ContextManager("test-session")
        ctx.set("test_key", "test_value")
        ctx.add_message("user", "test")
        
        ctx.reset()
        
        assert ctx.get("test_key") is None
        assert len(ctx.get_history()) == 0


class TestChatbot:
    """Tests for main chatbot."""
    
    def test_create_session(self):
        from src.agents import RetailChatbot
        
        chatbot = RetailChatbot()
        session = chatbot.create_session("CUST-TEST")
        
        assert session.customer_id == "CUST-TEST"
        assert session.session_id.startswith("SES-")
    
    def test_chat_response(self):
        from src.agents import RetailChatbot
        
        chatbot = RetailChatbot()
        
        response = chatbot.chat(
            "Do you have iPhones?",
            customer_id="CUST-TEST"
        )
        
        assert "message" in response or "error" in response
