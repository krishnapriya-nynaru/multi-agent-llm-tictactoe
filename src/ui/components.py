"""
UI components for the Tic Tac Toe application.
"""

import streamlit as st
from typing import Tuple, Optional
from src.game.board import TicTacToeBoard


class UIComponents:
    """UI components for displaying game elements."""

    @staticmethod
    def display_board(board: TicTacToeBoard) -> None:
        """
        Display the Tic Tac Toe board using Streamlit.

        Args:
            board: TicTacToeBoard instance to display
        """
        board_html = '<div class="game-board">'

        for i in range(3):
            for j in range(3):
                cell_value = board.board[i][j]
                board_html += f'<div class="board-cell">{cell_value}</div>'

        board_html += "</div>"
        st.markdown(board_html, unsafe_allow_html=True)

    @staticmethod
    def show_agent_status(agent_name: str, status: str) -> None:
        """
        Display the current agent status.

        Args:
            agent_name: Name of the agent
            status: Status message to display
        """
        st.markdown(
            f"""<div class="agent-status">
                🤖 <b>{agent_name}</b>: {status}
            </div>""",
            unsafe_allow_html=True,
        )

    @staticmethod
    def show_thinking_indicator(player_num: str, model_name: str) -> None:
        """
        Display a thinking indicator for the current player.

        Args:
            player_num: Player number (1 or 2)
            model_name: Name of the model being used
        """
        st.markdown(
            f"""<div class="thinking-container">
                <div class="agent-thinking">
                    <div style="margin-right: 10px; display: inline-block;">🔄</div>
                    Player {player_num} ({model_name}) is thinking...
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    @staticmethod
    def create_mini_board_html(
        board_state: list, highlight_pos: Optional[Tuple[int, int]] = None, is_player1: bool = True
    ) -> str:
        """
        Create HTML for a mini board with player-specific highlighting.

        Args:
            board_state: Current state of the board
            highlight_pos: Position to highlight (row, col)
            is_player1: Whether this is player 1's move

        Returns:
            str: HTML string for the mini board
        """
        html = '<div class="mini-board">'
        for i in range(3):
            for j in range(3):
                highlight = (
                    f"highlight player{1 if is_player1 else 2}"
                    if highlight_pos and (i, j) == highlight_pos
                    else ""
                )
                html += f'<div class="mini-cell {highlight}">{board_state[i][j]}</div>'
        html += "</div>"
        return html

    @staticmethod
    def display_move_history() -> None:
        """Display the move history with mini boards in two columns."""
        st.markdown(
            '<h3 style="margin-bottom: 30px;">📜 Game History</h3>',
            unsafe_allow_html=True,
        )
        history_container = st.empty()

        if "move_history" in st.session_state and st.session_state.move_history:
            # Split moves into player 1 and player 2 moves
            p1_moves = []
            p2_moves = []
            current_board = [[" " for _ in range(3)] for _ in range(3)]

            # Process all moves first
            for move in st.session_state.move_history:
                row, col = map(int, move["move"].split(","))
                is_player1 = "Player 1" in move["player"]
                symbol = "X" if is_player1 else "O"
                current_board[row][col] = symbol
                board_copy = [row[:] for row in current_board]

                move_html = f"""<div class="move-entry player{1 if is_player1 else 2}">
                    {UIComponents.create_mini_board_html(board_copy, (row, col), is_player1)}
                    <div class="move-info">
                        <div class="move-number player{1 if is_player1 else 2}">Move #{move["number"]}</div>
                        <div>{move["player"]}</div>
                        <div style="font-size: 0.9em; color: #888">Position: ({row}, {col})</div>
                    </div>
                </div>"""

                if is_player1:
                    p1_moves.append(move_html)
                else:
                    p2_moves.append(move_html)

            max_moves = max(len(p1_moves), len(p2_moves))
            history_content = '<div class="history-grid">'

            # Left column (Player 1)
            history_content += '<div class="history-column-left">'
            for i in range(max_moves):
                if i < len(p1_moves):
                    history_content += p1_moves[i]
            history_content += "</div>"

            # Right column (Player 2)
            history_content += '<div class="history-column-right">'
            for i in range(max_moves):
                if i < len(p2_moves):
                    history_content += p2_moves[i]
            history_content += "</div>"

            history_content += "</div>"

            # Display the content
            history_container.markdown(history_content, unsafe_allow_html=True)
        else:
            history_container.markdown(
                """<div style="text-align: center; color: #666; padding: 20px;">
                    No moves yet. Start the game to see the history!
                </div>""",
                unsafe_allow_html=True,
            )

    @staticmethod
    def display_api_key_error(missing_keys: list) -> None:
        """
        Display an error message for missing API keys.

        Args:
            missing_keys: List of missing API key messages
        """
        st.error(
            f"""
        🔑 **Missing API Keys:**

        {chr(10).join(f"• {key}" for key in missing_keys)}

        **To fix this:**
        1. Create a `.env` file in this directory
        2. Add your API keys:
        ```
        NVIDIA_API_KEY=your_key_here
        GROQ_API_KEY=your_key_here
        ```
        3. Restart the app
        """
        )

    @staticmethod
    def show_win_celebration(winner_player: str) -> None:
        """
        Display a celebration animation when a player wins.

        Args:
            winner_player: The winning player ("X" or "O")
        """
        import random

        # Determine winner color
        winner_color = "#4facfe" if winner_player == "X" else "#f5576c"

        # Create a simpler, more reliable confetti effect
        confetti_pieces = []
        for i in range(30):  # Reduced from 50 to 30 for better performance
            left = random.randint(0, 100)
            delay = random.uniform(0, 1.5)
            duration = random.uniform(2.5, 3.5)
            confetti_pieces.append(
                f'<div class="confetti-piece" style="left:{left}%;background:{winner_color};animation-delay:{delay}s;animation-duration:{duration}s;"></div>'
            )

        # Create compact HTML
        confetti_html = f'<div class="celebration">{"".join(confetti_pieces)}</div>'

        # Display celebration in a container
        st.markdown(confetti_html, unsafe_allow_html=True)
