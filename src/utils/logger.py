"""
Logging utilities for the Retail Order Query Chatbot.
"""

import sys
import logging
from typing import Optional

from loguru import logger

from src.config import settings


class InterceptHandler(logging.Handler):
    """Handler to intercept standard logging and redirect to loguru."""
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure application logging."""
    level = log_level or settings.log_level
    
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
        level=level,
        colorize=True,
    )
    
    # File handler
    if settings.logs_dir:
        logger.add(
            str(settings.logs_dir / "retail_chatbot_{time}.log"),
            rotation="10 MB",
            retention="1 week",
            level=level,
        )
    
    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Suppress noisy loggers
    for logger_name in ["httpx", "httpcore", "openai"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str) -> "logger":
    """Get a logger instance."""
    return logger.bind(name=name)


# Setup on import
setup_logging()
