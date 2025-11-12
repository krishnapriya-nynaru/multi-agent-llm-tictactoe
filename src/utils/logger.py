"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional


class Logger:
    """Custom logger for the application."""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = "TicTacToe", level: int = logging.INFO) -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Name of the logger
            level: Logging level (default: INFO)

        Returns:
            logging.Logger: Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name, level)
        return cls._instance

    @staticmethod
    def _setup_logger(name: str, level: int) -> logging.Logger:
        """
        Setup and configure the logger.

        Args:
            name: Name of the logger
            level: Logging level

        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        if logger.handlers:
            logger.handlers.clear()

        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

        return logger


# Create a default logger instance
logger = Logger.get_logger()
