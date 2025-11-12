"""
Configuration settings for the Tic Tac Toe game application.
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""

    # API Keys
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Model configurations
    MODEL_OPTIONS: Dict[str, str] = {
        # NVIDIA Models
        "kimi-k2": "nvidia:moonshotai/kimi-k2-instruct-0905",
        "gpt-oss-20b": "nvidia:openai/gpt-oss-20b",
        "mistral-nemotron": "nvidia:mistralai/mistral-nemotron",
        "nemotron-nano-vl": "nvidia:nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
        "llama3-70b": "nvidia:meta/llama3-70b-instruct",
        "llama-3.1-8b": "nvidia:meta/llama-3.1-8b-instruct",
        "llama-3.3-70b": "nvidia:meta/llama-3.3-70b-instruct",
        "llama-3.2-3b": "nvidia:meta/llama-3.2-3b-instruct",
        # Groq Models
        "groq-llama-3.3-70b": "groq:llama-3.3-70b-versatile",
        "groq-llama-3.1-70b": "groq:llama-3.1-70b-versatile",
        "groq-llama-3.1-8b": "groq:llama-3.1-8b-instant",
        "groq-mixtral-8x7b": "groq:mixtral-8x7b-32768",
        "groq-gemma2-9b": "groq:gemma2-9b-it",
    }

    # API key requirements mapping
    REQUIRED_KEYS_INFO: Dict[str, str] = {
        # NVIDIA Models
        "kimi-k2": "NVIDIA_API_KEY",
        "gpt-oss-20b": "NVIDIA_API_KEY",
        "mistral-nemotron": "NVIDIA_API_KEY",
        "nemotron-nano-vl": "NVIDIA_API_KEY",
        "llama3-70b": "NVIDIA_API_KEY",
        "llama-3.1-8b": "NVIDIA_API_KEY",
        "llama-3.3-70b": "NVIDIA_API_KEY",
        "llama-3.2-3b": "NVIDIA_API_KEY",
        # Groq Models
        "groq-llama-3.3-70b": "GROQ_API_KEY",
        "groq-llama-3.1-70b": "GROQ_API_KEY",
        "groq-llama-3.1-8b": "GROQ_API_KEY",
        "groq-mixtral-8x7b": "GROQ_API_KEY",
        "groq-gemma2-9b": "GROQ_API_KEY",
    }

    # Model metadata for display
    MODEL_INFO: Dict[str, Dict[str, str]] = {
        # NVIDIA Models
        "kimi-k2": {"provider": "NVIDIA", "size": "Large", "speed": "⚡ Fast", "badge": "🟢"},
        "gpt-oss-20b": {"provider": "NVIDIA", "size": "20B", "speed": "⚡ Fast", "badge": "🟢"},
        "mistral-nemotron": {"provider": "NVIDIA", "size": "Large", "speed": "⚡⚡ Very Fast", "badge": "🟢"},
        "nemotron-nano-vl": {"provider": "NVIDIA", "size": "8B", "speed": "⚡⚡ Very Fast", "badge": "🟢"},
        "llama3-70b": {"provider": "NVIDIA", "size": "70B", "speed": "⚡ Fast", "badge": "🟢"},
        "llama-3.1-8b": {"provider": "NVIDIA", "size": "8B", "speed": "⚡⚡ Very Fast", "badge": "🟢"},
        "llama-3.3-70b": {"provider": "NVIDIA", "size": "70B", "speed": "⚡ Fast", "badge": "🟢"},
        "llama-3.2-3b": {"provider": "NVIDIA", "size": "3B", "speed": "⚡⚡⚡ Ultra Fast", "badge": "🟢"},
        # Groq Models
        "groq-llama-3.3-70b": {"provider": "GROQ", "size": "70B", "speed": "⚡⚡⚡ Ultra Fast", "badge": "🟣"},
        "groq-llama-3.1-70b": {"provider": "GROQ", "size": "70B", "speed": "⚡⚡⚡ Ultra Fast", "badge": "🟣"},
        "groq-llama-3.1-8b": {"provider": "GROQ", "size": "8B", "speed": "⚡⚡⚡⚡ Lightning", "badge": "🟣"},
        "groq-mixtral-8x7b": {"provider": "GROQ", "size": "8x7B", "speed": "⚡⚡⚡ Ultra Fast", "badge": "🟣"},
        "groq-gemma2-9b": {"provider": "GROQ", "size": "9B", "speed": "⚡⚡⚡ Ultra Fast", "badge": "🟣"},
    }

    # Default model selections
    DEFAULT_PLAYER_X_MODEL: str = "llama-3.3-70b"
    DEFAULT_PLAYER_O_MODEL: str = "llama-3.1-8b"

    # App configuration
    APP_TITLE: str = "Agent Tic Tac Toe"
    APP_ICON: str = "🎮"
    PAGE_LAYOUT: str = "wide"

    # Game constants
    BOARD_SIZE: int = 3
    EMPTY_CELL: str = " "
    PLAYER_X: str = "X"
    PLAYER_O: str = "O"

    # Debug mode
    DEBUG_MODE: bool = True

    @classmethod
    def validate_api_key(cls, model_key: str) -> bool:
        """
        Validate if the required API key is present for a given model.

        Args:
            model_key: The model key to validate

        Returns:
            bool: True if API key is present, False otherwise
        """
        required_key = cls.REQUIRED_KEYS_INFO.get(model_key)
        if required_key:
            return bool(os.getenv(required_key))
        return True

    @classmethod
    def get_missing_keys(cls, models: list) -> list:
        """
        Get list of missing API keys for given models.

        Args:
            models: List of model keys to check

        Returns:
            list: List of missing API key messages
        """
        missing_keys = []
        for model in models:
            required_key = cls.REQUIRED_KEYS_INFO.get(model)
            if required_key and not os.getenv(required_key):
                missing_keys.append(f"**{model}** requires `{required_key}`")
        return missing_keys


# Create a singleton instance
settings = Settings()
