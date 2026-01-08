"""
Main entry point for the Retail Order Query Chatbot.
"""

import sys
import asyncio
from datetime import datetime

import uvicorn
from loguru import logger

from src.config import settings


def setup_logging() -> None:
    """Configure application logging."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    if settings.logs_dir:
        logger.add(
            str(settings.logs_dir / "retail_chatbot_{time}.log"),
            rotation="10 MB",
            retention="1 week",
            level=settings.log_level,
        )


def run_api() -> None:
    """Run the FastAPI server."""
    from src.api import app
    
    logger.info(f"Starting Retail Chatbot API on {settings.api.host}:{settings.api.port}")
    
    uvicorn.run(
        "src.api:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.api.workers,
    )


def demo_chat() -> None:
    """Run a demo chat conversation."""
    from src.agents import RetailChatbot
    
    logger.info("Starting demo conversation...")
    
    chatbot = RetailChatbot()
    
    print("\n" + "="*60)
    print("🛒 Retail Chatbot - Demo Conversation")
    print("="*60 + "\n")
    
    # Demo conversations
    conversations = [
        "Do you have the iPhone 15 Pro in blue?",
        "What's the price for the 256GB version?",
        "Where is my order #12345?",
        "I want to return my recent purchase",
    ]
    
    session = chatbot.create_session(customer_id="DEMO-001")
    
    for message in conversations:
        print(f"👤 Customer: {message}")
        response = session.chat(message)
        print(f"🤖 Chatbot: {response.get('message', 'I can help with that!')}")
        print()
    
    print("="*60 + "\n")


def interactive_chat() -> None:
    """Run interactive chat mode."""
    from src.agents import RetailChatbot
    
    print("\n" + "="*60)
    print("🛒 Retail Chatbot - Interactive Mode")
    print("="*60)
    print("\nType 'quit' to exit\n")
    
    chatbot = RetailChatbot()
    session = chatbot.create_session(customer_id="INTERACTIVE-001")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nThank you for shopping with us! Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            response = session.chat(user_input)
            print(f"\n🤖 Chatbot: {response.get('message', 'I can help with that!')}\n")
            
            if response.get("products"):
                print("📦 Products found:")
                for product in response["products"][:3]:
                    print(f"  - {product.get('name', 'Product')}: ${product.get('price', 0)}")
                print()
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main application entry point."""
    setup_logging()
    
    logger.info(f"Retail Order Query Chatbot v{getattr(sys.modules['src'], '__version__', '1.0.0')}")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "api":
            run_api()
        elif command == "demo":
            demo_chat()
        elif command == "chat":
            interactive_chat()
        else:
            print(f"Unknown command: {command}")
            print("\nUsage: python -m src.main [command]")
            print("\nCommands:")
            print("  api   - Run the API server")
            print("  demo  - Run demo conversation")
            print("  chat  - Interactive chat mode")
            sys.exit(1)
    else:
        # Default: run API
        run_api()


if __name__ == "__main__":
    main()
