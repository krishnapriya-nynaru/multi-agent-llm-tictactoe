"""
Tic Tac Toe game board implementation.
"""

from typing import List, Optional, Tuple
from src.config.settings import settings
from src.utils.logger import logger


class TicTacToeBoard:
    """Represents a Tic Tac Toe game board."""

    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.board = [[settings.EMPTY_CELL for _ in range(settings.BOARD_SIZE)] for _ in range(settings.BOARD_SIZE)]
        self.current_player = settings.PLAYER_X
        logger.info("Initialized new Tic Tac Toe board")

    def make_move(self, row: int, col: int) -> Tuple[bool, str]:
        """
        Make a move on the board.

        Args:
            row: Row index (0-2)
            col: Column index (0-2)

        Returns:
            Tuple[bool, str]: (Success status, Message with current board state or error)
        """
        # Validate move coordinates
        if not (0 <= row <= 2 and 0 <= col <= 2):
            error_msg = "Invalid move: Position out of bounds. Please choose row and column between 0 and 2."
            logger.warning(f"{error_msg} - Attempted: ({row}, {col})")
            return False, error_msg

        # Check if position is already occupied
        if self.board[row][col] != settings.EMPTY_CELL:
            error_msg = f"Invalid move: Position ({row}, {col}) is already occupied."
            logger.warning(error_msg)
            return False, error_msg

        # Make the move
        self.board[row][col] = self.current_player
        logger.info(f"Player {self.current_player} placed at position ({row}, {col})")

        # Get board state
        board_state = self.get_board_state()

        # Switch player
        self.current_player = settings.PLAYER_O if self.current_player == settings.PLAYER_X else settings.PLAYER_X

        return True, f"Move successful!\n{board_state}"

    def get_board_state(self) -> str:
        """
        Returns a string representation of the current board state.

        Returns:
            str: Board state as a formatted string
        """
        board_str = "\n-------------\n"
        for row in self.board:
            board_str += f"| {' | '.join(row)} |\n-------------\n"
        return board_str

    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner.

        Returns:
            Optional[str]: The winning player (X or O) or None if no winner
        """
        # Check rows
        for row in self.board:
            if row.count(row[0]) == settings.BOARD_SIZE and row[0] != settings.EMPTY_CELL:
                logger.info(f"Winner found: Player {row[0]} (row victory)")
                return row[0]

        # Check columns
        for col in range(settings.BOARD_SIZE):
            column = [self.board[row][col] for row in range(settings.BOARD_SIZE)]
            if column.count(column[0]) == settings.BOARD_SIZE and column[0] != settings.EMPTY_CELL:
                logger.info(f"Winner found: Player {column[0]} (column victory)")
                return column[0]

        # Check diagonals
        diagonal1 = [self.board[i][i] for i in range(settings.BOARD_SIZE)]
        if diagonal1.count(diagonal1[0]) == settings.BOARD_SIZE and diagonal1[0] != settings.EMPTY_CELL:
            logger.info(f"Winner found: Player {diagonal1[0]} (diagonal victory)")
            return diagonal1[0]

        diagonal2 = [self.board[i][settings.BOARD_SIZE - 1 - i] for i in range(settings.BOARD_SIZE)]
        if diagonal2.count(diagonal2[0]) == settings.BOARD_SIZE and diagonal2[0] != settings.EMPTY_CELL:
            logger.info(f"Winner found: Player {diagonal2[0]} (diagonal victory)")
            return diagonal2[0]

        return None

    def is_board_full(self) -> bool:
        """
        Check if the board is full (draw condition).

        Returns:
            bool: True if board is full, False otherwise
        """
        is_full = all(cell != settings.EMPTY_CELL for row in self.board for cell in row)
        if is_full:
            logger.info("Board is full - game ends in a draw")
        return is_full

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Get a list of valid moves (empty positions).

        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples representing valid moves
        """
        valid_moves = []
        for row in range(settings.BOARD_SIZE):
            for col in range(settings.BOARD_SIZE):
                if self.board[row][col] == settings.EMPTY_CELL:
                    valid_moves.append((row, col))
        return valid_moves

    def get_game_state(self) -> Tuple[bool, str]:
        """
        Get the current game state.

        Returns:
            Tuple[bool, str]: (is_game_over, status_message)
        """
        winner = self.check_winner()
        if winner:
            return True, f"Player {winner} wins!"

        if self.is_board_full():
            return True, "It's a draw!"

        return False, "Game in progress"

    def reset(self):
        """Reset the board to initial state."""
        self.board = [[settings.EMPTY_CELL for _ in range(settings.BOARD_SIZE)] for _ in range(settings.BOARD_SIZE)]
        self.current_player = settings.PLAYER_X
        logger.info("Board reset to initial state")
