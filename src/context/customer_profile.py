"""
Customer Profile for the Retail Order Query Chatbot.

Manages customer data and preferences.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.utils.logger import get_logger

logger = get_logger(__name__)


class CustomerProfile:
    """
    Manages customer profile and preferences.
    
    Tracks:
    - Customer info
    - Purchase history
    - Preferences
    - Loyalty status
    """
    
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        
        # Customer info
        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.phone: Optional[str] = None
        
        # Loyalty and status
        self.loyalty_tier: str = "bronze"  # bronze, silver, gold, platinum
        self.member_since: Optional[datetime] = None
        
        # Preferences
        self.preferences: Dict[str, Any] = {
            "favorite_categories": [],
            "preferred_brands": [],
            "size_preferences": {},
            "notification_preferences": {
                "email": True,
                "sms": True,
                "push": True,
            },
        }
        
        # History
        self.recent_orders: List[str] = []
        self.recent_views: List[str] = []
        self.wishlist: List[str] = []
    
    def load_from_database(self) -> None:
        """Load customer profile from database."""
        # Mock data for demo
        self.name = "John Doe"
        self.email = "john.doe@email.com"
        self.loyalty_tier = "gold"
        self.preferences["favorite_categories"] = ["Electronics", "Audio"]
        self.recent_orders = ["ORD-12345", "ORD-12344"]
        logger.info(f"Loaded profile for customer {self.customer_id}")
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update a preference."""
        if "." in key:
            parts = key.split(".")
            target = self.preferences
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value
        else:
            self.preferences[key] = value
    
    def add_to_history(self, history_type: str, item_id: str) -> None:
        """Add item to history."""
        if history_type == "order":
            if item_id not in self.recent_orders:
                self.recent_orders.insert(0, item_id)
                self.recent_orders = self.recent_orders[:20]
        elif history_type == "view":
            if item_id not in self.recent_views:
                self.recent_views.insert(0, item_id)
                self.recent_views = self.recent_views[:50]
    
    def add_to_wishlist(self, product_id: str) -> bool:
        """Add product to wishlist."""
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
            return True
        return False
    
    def remove_from_wishlist(self, product_id: str) -> bool:
        """Remove product from wishlist."""
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            return True
        return False
    
    def get_loyalty_benefits(self) -> Dict[str, Any]:
        """Get loyalty tier benefits."""
        benefits = {
            "bronze": {
                "discount": 0,
                "free_shipping_threshold": 50,
                "priority_support": False,
            },
            "silver": {
                "discount": 5,
                "free_shipping_threshold": 35,
                "priority_support": False,
            },
            "gold": {
                "discount": 10,
                "free_shipping_threshold": 0,
                "priority_support": True,
            },
            "platinum": {
                "discount": 15,
                "free_shipping_threshold": 0,
                "priority_support": True,
                "early_access": True,
            },
        }
        return benefits.get(self.loyalty_tier, benefits["bronze"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "loyalty_tier": self.loyalty_tier,
            "preferences": self.preferences,
            "recent_orders": self.recent_orders[:5],
            "wishlist_count": len(self.wishlist),
        }
    
    def __repr__(self) -> str:
        return f"CustomerProfile(id='{self.customer_id}', tier='{self.loyalty_tier}')"
