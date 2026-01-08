"""
Configuration management for the Retail Order Query Chatbot.
"""

from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    """LLM configuration settings."""
    
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=4096, alias="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(default=0.7, alias="OPENAI_TEMPERATURE")
    
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class VectorDBSettings(BaseSettings):
    """Vector database configuration."""
    
    pinecone_api_key: str = Field(default="", alias="PINECONE_API_KEY")
    pinecone_index: str = Field(default="products", alias="PINECONE_INDEX")
    pinecone_environment: str = Field(default="us-west1-gcp", alias="PINECONE_ENVIRONMENT")
    
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    database_url: str = Field(
        default="sqlite:///./data/retail.db",
        alias="DATABASE_URL"
    )
    pool_size: int = Field(default=10, alias="DATABASE_POOL_SIZE")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class ShopifySettings(BaseSettings):
    """Shopify integration settings."""
    
    store_url: str = Field(default="", alias="SHOPIFY_STORE_URL")
    access_token: str = Field(default="", alias="SHOPIFY_ACCESS_TOKEN")
    api_version: str = Field(default="2024-01", alias="SHOPIFY_API_VERSION")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class ShippingSettings(BaseSettings):
    """Shipping integration settings."""
    
    easypost_api_key: str = Field(default="", alias="EASYPOST_API_KEY")
    shipstation_api_key: str = Field(default="", alias="SHIPSTATION_API_KEY")
    shipstation_api_secret: str = Field(default="", alias="SHIPSTATION_API_SECRET")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class MessagingSettings(BaseSettings):
    """Messaging channel settings."""
    
    whatsapp_phone_number_id: str = Field(default="", alias="WHATSAPP_PHONE_NUMBER_ID")
    whatsapp_access_token: str = Field(default="", alias="WHATSAPP_ACCESS_TOKEN")
    
    facebook_page_access_token: str = Field(default="", alias="FACEBOOK_PAGE_ACCESS_TOKEN")
    
    twilio_account_sid: str = Field(default="", alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default="", alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(default="", alias="TWILIO_PHONE_NUMBER")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class AgentSettings(BaseSettings):
    """Agent configuration."""
    
    max_iterations: int = Field(default=15, alias="AGENT_MAX_ITERATIONS")
    timeout_seconds: int = Field(default=60, alias="AGENT_TIMEOUT_SECONDS")
    verbose: bool = Field(default=True, alias="AGENT_VERBOSE")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class SessionSettings(BaseSettings):
    """Session configuration."""
    
    ttl_hours: int = Field(default=24, alias="SESSION_TTL_HOURS")
    max_conversation_history: int = Field(default=50, alias="MAX_CONVERSATION_HISTORY")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class APISettings(BaseSettings):
    """API server configuration."""
    
    host: str = Field(default="0.0.0.0", alias="API_HOST")
    port: int = Field(default=8000, alias="API_PORT")
    workers: int = Field(default=4, alias="API_WORKERS")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        alias="CORS_ORIGINS"
    )
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class Settings(BaseSettings):
    """Main application settings."""
    
    app_name: str = Field(default="retail-chatbot", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Sub-settings
    llm: LLMSettings = Field(default_factory=LLMSettings)
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    shopify: ShopifySettings = Field(default_factory=ShopifySettings)
    shipping: ShippingSettings = Field(default_factory=ShippingSettings)
    messaging: MessagingSettings = Field(default_factory=MessagingSettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    session: SessionSettings = Field(default_factory=SessionSettings)
    api: APISettings = Field(default_factory=APISettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent
    
    @property
    def data_dir(self) -> Path:
        """Get data directory."""
        data_path = self.project_root / "data"
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path
    
    @property
    def logs_dir(self) -> Path:
        """Get logs directory."""
        logs_path = self.project_root / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        return logs_path


# Global settings instance
settings = Settings()
