---
description: Quick start the Retail Order Query Chatbot project
---

# Quick Start Workflow

## Prerequisites Check

1. Ensure Python 3.14+ is installed
2. Ensure you have an OpenAI API key

## Setup Steps

// turbo

1. Navigate to project directory:

```bash
cd /Users/gopalsaini/Documents/Source/ai-agents-playgrounds/case-studies/case-studies/retail-order-query-chatbot
```

// turbo 2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

// turbo 3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Then edit `.env` and add your `OPENAI_API_KEY`.

// turbo 5. Run the API server:

```bash
python -m src.main api
```

The API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

## Alternative Run Modes

// turbo

- **Demo conversation:**

```bash
python -m src.main demo
```

// turbo

- **Interactive chat:**

```bash
python -m src.main chat
```

## Docker Setup (Alternative)

// turbo

1. Start all services with Docker:

```bash
docker-compose up --build
```

This starts: API server, PostgreSQL, Redis, Qdrant

## Running Tests

// turbo

```bash
pytest
```

// turbo
With coverage:

```bash
pytest --cov=src --cov-report=html
```

## Sample Conversations

Try these messages in the chatbot:

1. Product Query: "Do you have the iPhone 15 Pro in blue?"
2. Order Tracking: "Where is my order #12345?"
3. Cart Help: "Apply coupon SAVE10 to my cart"
4. Returns: "I want to return my recent purchase"
5. Recommendations: "What do you recommend for me?"

## Project Context

For full project context and architecture details, see:
`.agent/project-context.md`
