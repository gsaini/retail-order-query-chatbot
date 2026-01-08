"""
Session Manager for the Retail Order Query Chatbot.

Manages chat sessions with optional Redis persistence.
"""

from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import json
import uuid

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    """
    Manages chat sessions.
    
    Provides session creation, retrieval, and cleanup.
    Can optionally persist to Redis.
    """
    
    def __init__(self, use_redis: bool = False):
        self.use_redis = use_redis
        self.ttl_hours = settings.session.ttl_hours
        
        # In-memory session store (fallback)
        self._sessions: Dict[str, Dict[str, Any]] = {}
        
        # Redis client (if enabled)
        self._redis = None
        if use_redis:
            try:
                import redis
                self._redis = redis.from_url(settings.database.redis_url)
                logger.info("Session manager connected to Redis")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Using in-memory storage.")
                self.use_redis = False
    
    def create_session(self, customer_id: str) -> Dict[str, Any]:
        """
        Create a new session.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Session data
        """
        session_id = f"SES-{uuid.uuid4().hex[:12].upper()}"
        
        session = {
            "session_id": session_id,
            "customer_id": customer_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "message_count": 0,
            "context": {},
        }
        
        self._save_session(session_id, session)
        
        logger.info(f"Created session {session_id} for customer {customer_id}")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get an existing session."""
        return self._load_session(session_id)
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """Update session data."""
        session = self._load_session(session_id)
        if session:
            session.update(data)
            session["last_activity"] = datetime.utcnow().isoformat()
            self._save_session(session_id, session)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if self.use_redis and self._redis:
            self._redis.delete(f"session:{session_id}")
        else:
            self._sessions.pop(session_id, None)
        
        logger.info(f"Deleted session {session_id}")
        return True
    
    def _save_session(self, session_id: str, session: Dict[str, Any]) -> None:
        """Save session to storage."""
        if self.use_redis and self._redis:
            self._redis.setex(
                f"session:{session_id}",
                timedelta(hours=self.ttl_hours),
                json.dumps(session)
            )
        else:
            self._sessions[session_id] = session
    
    def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from storage."""
        if self.use_redis and self._redis:
            data = self._redis.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return None
        else:
            return self._sessions.get(session_id)
    
    def cleanup_expired(self) -> int:
        """Clean up expired sessions (in-memory only)."""
        if self.use_redis:
            return 0  # Redis handles TTL automatically
        
        expired = []
        cutoff = datetime.utcnow() - timedelta(hours=self.ttl_hours)
        
        for session_id, session in self._sessions.items():
            last_activity = datetime.fromisoformat(session["last_activity"])
            if last_activity < cutoff:
                expired.append(session_id)
        
        for session_id in expired:
            del self._sessions[session_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        
        return len(expired)
    
    def get_active_count(self) -> int:
        """Get count of active sessions."""
        if self.use_redis and self._redis:
            keys = self._redis.keys("session:*")
            return len(keys)
        return len(self._sessions)
