# Retail Order Query Chatbot - Project Context

> **Last Updated:** 2026-01-07
> **Author:** Gopal Saini

## Overview

The Retail Order Query Chatbot is a **multi-agent AI system** that enables dynamic, context-aware interactions to assist customers with product queries and order tracking, improving the overall shopping experience.

## Technology Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Language        | Python 3.14+          |
| Agent Framework | LangGraph, LangChain  |
| LLM Provider    | OpenAI GPT-4 / Claude |
| Vector DB       | Pinecone / Qdrant     |
| API Framework   | FastAPI               |
| Session Store   | Redis                 |
| Database        | PostgreSQL            |

## Project Structure

```
retail-order-query-chatbot/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point (API, demo, chat modes)
│   ├── config.py                # Configuration management
│   │
│   ├── agents/                  # 🤖 Multi-Agent System
│   │   ├── __init__.py
│   │   ├── base.py              # Base agent class
│   │   ├── orchestrator.py      # RetailOrchestrator & RetailChatbot
│   │   ├── router_agent.py      # Intent classification & routing
│   │   ├── product_agent.py     # Product queries & search
│   │   ├── order_agent.py       # Order tracking
│   │   ├── recommendation_agent.py  # Product recommendations
│   │   ├── support_agent.py     # Returns & refunds
│   │   └── checkout_agent.py    # Cart & checkout
│   │
│   ├── api/                     # 🌐 FastAPI REST API
│   │   ├── __init__.py
│   │   ├── routes.py            # All API endpoints
│   │   └── schemas.py           # Request/response models
│   │
│   ├── context/                 # 📝 Context Management
│   │   ├── __init__.py
│   │   ├── context_manager.py   # Conversation context
│   │   ├── session_manager.py   # Session handling
│   │   └── customer_profile.py  # Customer data
│   │
│   └── utils/                   # 🛠️ Utilities
│       ├── __init__.py
│       ├── logger.py
│       ├── formatters.py
│       └── validators.py
│
├── tests/
│   ├── __init__.py
│   ├── test_unit.py
│   └── test_integration.py
│
├── config/
│   ├── agents.yaml
│   └── channels.yaml
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Agent Architecture

```
                    ┌─────────────────┐
                    │   Router Agent  │
                    │ (Intent & Route)│
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Product  │      │  Order   │      │  Support │
    │  Agent   │      │  Agent   │      │  Agent   │
    └──────────┘      └──────────┘      └──────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Product  │      │  Order   │      │  Ticket  │
    │ Catalog  │      │  System  │      │  System  │
    └──────────┘      └──────────┘      └──────────┘
```

## Agent Responsibilities

| Agent                   | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| **RouterAgent**         | Classify intent, route to appropriate agent        |
| **ProductAgent**        | Search products, check inventory, compare items    |
| **OrderAgent**          | Track orders, shipping updates, delivery estimates |
| **RecommendationAgent** | Personalized suggestions, cross-sell, upsell       |
| **SupportAgent**        | Returns, refunds, exchanges, complaints            |
| **CheckoutAgent**       | Cart management, coupons, checkout assistance      |

## API Endpoints

| Endpoint                       | Method | Description         |
| ------------------------------ | ------ | ------------------- |
| `/api/v1/chat`                 | POST   | Main chat endpoint  |
| `/api/v1/products/search`      | POST   | Search products     |
| `/api/v1/products/{id}`        | GET    | Product details     |
| `/api/v1/orders/track`         | POST   | Track order         |
| `/api/v1/cart/{customer_id}`   | GET    | Get cart            |
| `/api/v1/cart/coupon`          | POST   | Apply coupon        |
| `/api/v1/returns`              | POST   | Create return       |
| `/api/v1/recommendations/{id}` | GET    | Get recommendations |

## Running the Application

```bash
# API Server
python -m src.main api

# Demo conversation
python -m src.main demo

# Interactive chat
python -m src.main chat

# Docker
docker-compose up --build
```

## Context-Aware Interactions

The chatbot maintains conversation context:

```
Turn 1: "Show me Nike running shoes"
        → Context: {product_type: "running_shoes", brand: "Nike"}

Turn 2: "In size 10"
        → Context: {product_type: "running_shoes", brand: "Nike", size: 10}

Turn 3: "Under $150"
        → Context: {product_type: "running_shoes", brand: "Nike", size: 10, max_price: 150}

Turn 4: "Add the first one to cart"
        → Context preserved, adds product to cart
```

## Related Projects

This project follows the same architecture as:

- Financial Research Analyst Agent
- Healthcare Startup Application
- Travel Agent Application
