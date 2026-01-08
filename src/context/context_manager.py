"""
Context Manager for the Retail Order Query Chatbot.

Manages conversation context and state across interactions.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ContextManager:
    """
    Manages conversation context for a chat session.
    
    Tracks:
    - Conversation history
    - Current topic/focus
    - Extracted entities
    - User preferences
    - Cart state
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.utcnow()
        
        # Core context data
        self._context: Dict[str, Any] = {
            "customer_id": None,
            "current_topic": None,
            "product_focus": None,
            "filters": {},
            "cart_items": [],
            "last_intent": None,
        }
        
        # Conversation history
        self._history: List[Dict[str, Any]] = []
        
        # Extracted entities from conversation
        self._entities: Dict[str, Any] = {
            "mentioned_products": [],
            "mentioned_orders": [],
            "preferences": {},
        }
    
    def set(self, key: str, value: Any) -> None:
        """Set a context value."""
        self._context[key] = value
        logger.debug(f"Context set: {key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a context value."""
        return self._context.get(key, default)
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self._history.append(message)
        
        # Limit history size
        max_history = settings.session.max_conversation_history
        if len(self._history) > max_history:
            self._history = self._history[-max_history:]
        
        logger.debug(f"Added message from {role}")
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        return self._history[-limit:]
    
    def set_entity(self, entity_type: str, value: Any) -> None:
        """Set an extracted entity."""
        if entity_type in ["mentioned_products", "mentioned_orders"]:
            if value not in self._entities[entity_type]:
                self._entities[entity_type].append(value)
        else:
            self._entities[entity_type] = value
    
    def get_entity(self, entity_type: str, default: Any = None) -> Any:
        """Get an extracted entity."""
        return self._entities.get(entity_type, default)
    
    def update_topic(self, topic: str, focus: Optional[str] = None) -> None:
        """Update current conversation topic."""
        self._context["current_topic"] = topic
        if focus:
            self._context["product_focus"] = focus
    
    def add_filter(self, key: str, value: Any) -> None:
        """Add a search filter."""
        self._context["filters"][key] = value
    
    def clear_filters(self) -> None:
        """Clear all search filters."""
        self._context["filters"] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for agent use."""
        return {
            "session_id": self.session_id,
            "context": self._context,
            "entities": self._entities,
            "history": self.get_history(5),
            "created_at": self.created_at.isoformat(),
        }
    
    def reset(self) -> None:
        """Reset context to initial state."""
        customer_id = self._context.get("customer_id")
        self._context = {
            "customer_id": customer_id,
            "current_topic": None,
            "product_focus": None,
            "filters": {},
            "cart_items": [],
            "last_intent": None,
        }
        self._history = []
        self._entities = {
            "mentioned_products": [],
            "mentioned_orders": [],
            "preferences": {},
        }
        logger.info(f"Context reset for session {self.session_id}")
    
    def __repr__(self) -> str:
        return f"ContextManager(session='{self.session_id}', messages={len(self._history)})"
