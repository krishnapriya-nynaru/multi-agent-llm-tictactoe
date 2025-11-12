"""
Tic Tac Toe agent implementation.
"""

from textwrap import dedent
from typing import Tuple
from agno.agent import Agent
from agno.models.nvidia import Nvidia
from agno.models.groq import Groq
from src.config.settings import settings
from src.utils.logger import logger


class TicTacToeAgentFactory:
    """Factory class for creating Tic Tac Toe agents."""

    @staticmethod
    def get_model_for_provider(provider: str, model_name: str):
        """
        Creates and returns the appropriate model instance based on the provider.

        Args:
            provider: The model provider ('nvidia' or 'groq')
            model_name: The specific model name/ID

        Returns:
            An instance of the appropriate model class (Nvidia or Groq)

        Raises:
            ValueError: If the provider is not supported
        """
        if provider == "nvidia":
            logger.info(f"Creating NVIDIA model: {model_name}")
            return Nvidia(id=model_name)
        elif provider == "groq":
            logger.info(f"Creating Groq model: {model_name}")
            return Groq(id=model_name)
        else:
            error_msg = f"Unsupported model provider: {provider}. Supported providers: 'nvidia', 'groq'"
            logger.error(error_msg)
            raise ValueError(error_msg)

    @classmethod
    def create_player_agent(cls, player_name: str, player_symbol: str, model_str: str, debug_mode: bool = True) -> Agent:
        """
        Create a player agent for Tic Tac Toe.

        Args:
            player_name: Name of the player (e.g., "Player X")
            player_symbol: Symbol used by the player ("X" or "O")
            model_str: Model string in format "provider:model_name"
            debug_mode: Enable debug logging

        Returns:
            Agent: Configured agent instance
        """
        # Parse model provider and name
        provider, model_name = model_str.split(":")
        model = cls.get_model_for_provider(provider, model_name)

        agent = Agent(
            name=player_name,
            description=dedent(f"""\
            You are {player_name} in a Tic Tac Toe game. Your goal is to win by placing three {player_symbol}'s in a row (horizontally, vertically, or diagonally).

            BOARD LAYOUT:
            - The board is a 3x3 grid with coordinates from (0,0) to (2,2)
            - Top-left is (0,0), bottom-right is (2,2)

            RULES:
            - You can only place {player_symbol} in empty spaces (shown as " " on the board)
            - Players take turns placing their marks
            - First to get 3 marks in a row (horizontal, vertical, or diagonal) wins
            - If all spaces are filled with no winner, the game is a draw

            YOUR RESPONSE:
            - Provide ONLY two numbers separated by a space (row column)
            - Example: "1 2" places your {player_symbol} in row 1, column 2
            - Choose only from the valid moves list provided to you

            STRATEGY TIPS:
            - Study the board carefully and make strategic moves
            - Block your opponent's potential winning moves
            - Create opportunities for multiple winning paths
            - Pay attention to the valid moves and avoid illegal moves
            """),
            model=model,
            debug_mode=debug_mode,
        )

        logger.info(f"Created {player_name} agent with model {model_name}")
        return agent

    @classmethod
    def get_tic_tac_toe_players(
        cls,
        model_x: str = None,
        model_o: str = None,
        debug_mode: bool = True,
    ) -> Tuple[Agent, Agent]:
        """
        Returns instances of the Tic Tac Toe Player Agents.

        Args:
            model_x: Model string for player X (format: "provider:model_name")
            model_o: Model string for player O (format: "provider:model_name")
            debug_mode: Enable logging and debug features

        Returns:
            Tuple[Agent, Agent]: (player_x, player_o) agent instances
        """
        # Use default models if not provided
        if model_x is None:
            model_x = settings.MODEL_OPTIONS[settings.DEFAULT_PLAYER_X_MODEL]
        if model_o is None:
            model_o = settings.MODEL_OPTIONS[settings.DEFAULT_PLAYER_O_MODEL]

        logger.info(f"Creating Tic Tac Toe players - X: {model_x}, O: {model_o}")

        player_x = cls.create_player_agent("Player X", "X", model_x, debug_mode)
        player_o = cls.create_player_agent("Player O", "O", model_o, debug_mode)

        return player_x, player_o
