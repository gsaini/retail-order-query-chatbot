"""
Orchestrator for the Retail Order Query Chatbot.

Main orchestrator that coordinates all specialized agents.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid
import asyncio

from src.agents.base import BaseAgent, AgentResult
from src.agents.router_agent import RouterAgent, CustomerIntent
from src.agents.product_agent import ProductAgent
from src.agents.order_agent import OrderAgent
from src.agents.recommendation_agent import RecommendationAgent
from src.agents.support_agent import SupportAgent
from src.agents.checkout_agent import CheckoutAgent
from src.context.context_manager import ContextManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RetailOrchestrator:
    """
    Main orchestrator for the retail chatbot.
    
    Coordinates routing and execution across all specialized agents.
    """
    
    def __init__(self):
        # Initialize all agents
        self.router = RouterAgent()
        self.product_agent = ProductAgent()
        self.order_agent = OrderAgent()
        self.recommendation_agent = RecommendationAgent()
        self.support_agent = SupportAgent()
        self.checkout_agent = CheckoutAgent()
        
        # Agent registry
        self.agents = {
            "RouterAgent": self.router,
            "ProductAgent": self.product_agent,
            "OrderAgent": self.order_agent,
            "RecommendationAgent": self.recommendation_agent,
            "SupportAgent": self.support_agent,
            "CheckoutAgent": self.checkout_agent,
        }
        
        logger.info("RetailOrchestrator initialized with all agents")
    
    async def process_message(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a customer message through the agent pipeline.
        
        Args:
            message: Customer message
            context: Conversation context
            
        Returns:
            Response from appropriate agent
        """
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Route the message
            routing = await self.router.route(message, context)
            target_agent_name = routing["target_agent"]
            intent = routing["intent"]
            
            logger.info(f"Routing to {target_agent_name} (intent: {intent})")
            
            # Step 2: Get the target agent
            target_agent = self.agents.get(target_agent_name)
            
            if not target_agent:
                return {
                    "success": False,
                    "message": "I'm sorry, I couldn't understand your request. Could you please rephrase?",
                    "error": f"Unknown agent: {target_agent_name}"
                }
            
            # Step 3: Execute with the target agent
            result = await target_agent.execute(message, context)
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                "success": result.success,
                "message": result.message or result.data.get("output", ""),
                "data": result.data,
                "intent": intent,
                "agent": target_agent_name,
                "execution_time": execution_time
            }
            
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {
                "success": False,
                "message": "I apologize, but I encountered an error. Please try again.",
                "error": str(e)
            }
    
    def process_message_sync(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Synchronous version of process_message."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.process_message(message, context))


class ChatSession:
    """
    A single chat session with a customer.
    
    Maintains context and conversation history.
    """
    
    def __init__(
        self,
        session_id: str,
        customer_id: str,
        orchestrator: RetailOrchestrator
    ):
        self.session_id = session_id
        self.customer_id = customer_id
        self.orchestrator = orchestrator
        self.context_manager = ContextManager(session_id)
        self.created_at = datetime.utcnow()
        
        # Initialize context with customer info
        self.context_manager.set("customer_id", customer_id)
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Send a message and get a response.
        
        Args:
            message: Customer message
            
        Returns:
            Chatbot response
        """
        # Add message to history
        self.context_manager.add_message("user", message)
        
        # Get context for the orchestrator
        context = self.context_manager.to_dict()
        
        # Process message
        response = self.orchestrator.process_message_sync(message, context)
        
        # Add response to history
        if response.get("success"):
            self.context_manager.add_message("assistant", response["message"])
        
        # Update context based on response
        if response.get("data", {}).get("products"):
            self.context_manager.set("last_products", response["data"]["products"])
        
        return response
    
    async def chat_async(self, message: str) -> Dict[str, Any]:
        """Async version of chat."""
        self.context_manager.add_message("user", message)
        context = self.context_manager.to_dict()
        
        response = await self.orchestrator.process_message(message, context)
        
        if response.get("success"):
            self.context_manager.add_message("assistant", response["message"])
        
        return response
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.context_manager.get_history()


class RetailChatbot:
    """
    High-level interface for the retail chatbot.
    
    Provides easy-to-use methods for chat interactions.
    """
    
    def __init__(self):
        self.orchestrator = RetailOrchestrator()
        self.sessions: Dict[str, ChatSession] = {}
    
    def create_session(self, customer_id: str) -> ChatSession:
        """
        Create a new chat session.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            New ChatSession instance
        """
        session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"
        session = ChatSession(session_id, customer_id, self.orchestrator)
        self.sessions[session_id] = session
        
        logger.info(f"Created session {session_id} for customer {customer_id}")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get an existing session."""
        return self.sessions.get(session_id)
    
    def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        customer_id: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Simple chat interface.
        
        Args:
            message: Customer message
            session_id: Existing session ID or None for new session
            customer_id: Customer ID for new sessions
            
        Returns:
            Chatbot response
        """
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            session = self.create_session(customer_id)
        
        return session.chat(message)
