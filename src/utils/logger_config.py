"""
Logger configuration for the project.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
    from loguru import logger as loguru_logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    if LOGURU_AVAILABLE:
        return LoguruAdapter(name)
    else:
        return setup_standard_logger(name, level)


def setup_standard_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Setup standard Python logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Set level
        logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate logs
        logger.propagate = False
    
    return logger


class LoguruAdapter:
    """Adapter to make loguru compatible with standard logging interface."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = loguru_logger
    
    def info(self, message: str, *args, **kwargs):
        self.logger.info(f"[{self.name}] {message}", *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(f"[{self.name}] {message}", *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(f"[{self.name}] {message}", *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.logger.error(f"[{self.name}] {message}", *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(f"[{self.name}] {message}", *args, **kwargs)


def configure_logging(
    log_file: Optional[Path] = None,
    level: str = "INFO",
    rotation: str = "10 MB",
    retention: str = "30 days"
):
    """Configure global logging settings."""
    if LOGURU_AVAILABLE:
        # Remove default handler
        loguru_logger.remove()
        
        # Add console handler
        loguru_logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level=level
        )
        
        # Add file handler if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            loguru_logger.add(
                log_file,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                level=level,
                rotation=rotation,
                retention=retention
            )
    else:
        # Configure standard logging
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
