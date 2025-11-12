"""
Main entry point for the Tic Tac Toe Agent Game application.
"""

import re
import nest_asyncio
import streamlit as st
from agno.run.agent import RunOutput

# Apply nest_asyncio for proper async handling
nest_asyncio.apply()

# Import application modules
from src.config.settings import settings
from src.game.board import TicTacToeBoard
from src.agents.tic_tac_toe_agent import TicTacToeAgentFactory
from src.ui.styles import CUSTOM_CSS
from src.ui.components import UIComponents
from src.utils.logger import logger


class TicTacToeGame:
    """Main game controller for Tic Tac Toe."""

    def __init__(self):
        """Initialize the game controller."""
        self.ui = UIComponents()
        self.agent_factory = TicTacToeAgentFactory()

    def configure_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=settings.APP_TITLE,
            page_icon=settings.APP_ICON,
            layout=settings.PAGE_LAYOUT,
            initial_sidebar_state="expanded",
        )
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        logger.info("Page configured successfully")

    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "game_started" not in st.session_state:
            st.session_state.game_started = False
            st.session_state.game_paused = False
            st.session_state.move_history = []
            logger.info("Session state initialized")

        # Initialize statistics tracking
        if "session_stats" not in st.session_state:
            st.session_state.session_stats = {
                "total_games": 0,
                "x_wins": 0,
                "o_wins": 0,
                "draws": 0,
                "model_wins": {},  # Track wins per model
            }

        if "current_streak" not in st.session_state:
            st.session_state.current_streak = {"player": None, "count": 0}

    def render_header(self):
        """Render the main application header."""
        st.markdown(
            "<h1 class='main-title'>Watch Agents play Tic Tac Toe</h1>",
            unsafe_allow_html=True,
        )

    def render_sidebar(self) -> tuple:
        """
        Render the enhanced sidebar with game controls.

        Returns:
            tuple: (selected_p_x, selected_p_o, missing_keys)
        """
        with st.sidebar:
            # 🎮 BATTLE ARENA HEADER
            st.markdown("""
            <div style='text-align: center; padding: 20px 0 10px 0;'>
                <h2 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;
                           margin: 0; font-size: 1.8em;'>
                    🎮 AI BATTLE ARENA
                </h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # 🔵 PLAYER X MODEL CARD
            st.markdown("### 🔵 PLAYER X")
            selected_p_x = st.selectbox(
                "Choose Model",
                list(settings.MODEL_OPTIONS.keys()),
                index=list(settings.MODEL_OPTIONS.keys()).index(settings.DEFAULT_PLAYER_X_MODEL),
                key="model_p1",
                label_visibility="collapsed"
            )
            self._render_model_card(selected_p_x)

            st.markdown("<br>", unsafe_allow_html=True)

            # 🔴 PLAYER O MODEL CARD
            st.markdown("### 🔴 PLAYER O")
            selected_p_o = st.selectbox(
                "Choose Model",
                list(settings.MODEL_OPTIONS.keys()),
                index=list(settings.MODEL_OPTIONS.keys()).index(settings.DEFAULT_PLAYER_O_MODEL),
                key="model_p2",
                label_visibility="collapsed"
            )
            self._render_model_card(selected_p_o)

            st.markdown("---")

            # API Key validation
            missing_keys = settings.get_missing_keys([selected_p_x, selected_p_o])

            if missing_keys:
                self.ui.display_api_key_error(missing_keys)

            # ⚔️ MATCH CONTROLS
            st.markdown("### ⚔️ MATCH CONTROLS")
            self._render_game_controls(missing_keys)

            # 🎲 QUICK ACTIONS
            self._render_quick_actions(missing_keys)

            st.markdown("---")

            # 📊 SESSION STATS
            self._render_session_stats()

            st.markdown("---")

            # 🏆 TOP PERFORMERS
            self._render_leaderboard()

            st.markdown("---")

            # 💡 PRO TIP
            self._render_pro_tip()

        return selected_p_x, selected_p_o, missing_keys

    def _render_game_controls(self, missing_keys: list):
        """Render game control buttons."""
        col1, col2 = st.columns(2)

        with col1:
            if not st.session_state.game_started:
                if st.button("▶️ Start Game", disabled=bool(missing_keys), use_container_width=True):
                    self._start_new_game()
            else:
                game_over, _ = st.session_state.game_board.get_game_state()
                if not game_over:
                    if st.button(
                        "⏸️ Pause" if not st.session_state.game_paused else "▶️ Resume",
                        use_container_width=True
                    ):
                        st.session_state.game_paused = not st.session_state.game_paused
                        st.rerun()

        with col2:
            if st.session_state.game_started:
                if st.button("🔄 New Game", use_container_width=True):
                    self._start_new_game()

    def _start_new_game(self):
        """Start a new game."""
        model_x = settings.MODEL_OPTIONS[st.session_state.model_p1]
        model_o = settings.MODEL_OPTIONS[st.session_state.model_p2]

        st.session_state.player_x, st.session_state.player_o = (
            self.agent_factory.get_tic_tac_toe_players(
                model_x=model_x,
                model_o=model_o,
                debug_mode=settings.DEBUG_MODE,
            )
        )
        st.session_state.game_board = TicTacToeBoard()
        st.session_state.game_started = True
        st.session_state.game_paused = False
        st.session_state.move_history = []
        logger.info("New game started")
        st.rerun()

    def _render_model_card(self, model_key: str):
        """Render a model information card."""
        info = settings.MODEL_INFO.get(model_key, {})
        provider = info.get("provider", "Unknown")
        size = info.get("size", "N/A")
        speed = info.get("speed", "N/A")
        badge = info.get("badge", "⚪")

        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px;
                    border-left: 4px solid {"#4facfe" if badge == "🟢" else "#764ba2"};
                    margin: 8px 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 600;'>{badge} {provider}</span>
                <span style='font-size: 0.85em; color: #888;'>Model {size}</span>
            </div>
            <div style='margin-top: 8px; font-size: 0.9em;'>
                {speed}
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_quick_actions(self, missing_keys: list):
        """Render quick action buttons."""
        st.markdown("### 🎲 QUICK ACTIONS")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🎲 Random", help="Pick random models", use_container_width=True, disabled=bool(missing_keys)):
                import random
                models = list(settings.MODEL_OPTIONS.keys())
                st.session_state.model_p1 = random.choice(models)
                st.session_state.model_p2 = random.choice(models)
                st.rerun()

        with col2:
            if st.button("📊 Reset Stats", help="Clear session statistics", use_container_width=True):
                st.session_state.session_stats = {
                    "total_games": 0,
                    "x_wins": 0,
                    "o_wins": 0,
                    "draws": 0,
                    "model_wins": {},
                }
                st.session_state.current_streak = {"player": None, "count": 0}
                st.rerun()

    def _render_session_stats(self):
        """Render session statistics."""
        stats = st.session_state.session_stats
        total = stats["total_games"]

        st.markdown("### 📊 SESSION STATS")

        if total > 0:
            x_pct = (stats["x_wins"] / total) * 100
            o_pct = (stats["o_wins"] / total) * 100
            draw_pct = (stats["draws"] / total) * 100

            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 16px; border-radius: 12px;'>
                <div style='margin-bottom: 12px;'>
                    <strong>Games Played:</strong> {total}
                </div>
                <div style='margin-bottom: 8px;'>
                    🔵 X Wins: <strong>{stats["x_wins"]}</strong> ({x_pct:.1f}%)
                </div>
                <div style='margin-bottom: 8px;'>
                    🔴 O Wins: <strong>{stats["o_wins"]}</strong> ({o_pct:.1f}%)
                </div>
                <div style='margin-bottom: 12px;'>
                    🤝 Draws: <strong>{stats["draws"]}</strong> ({draw_pct:.1f}%)
                </div>
                {self._get_streak_display()}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🎮 No games played yet. Start your first match!")

    def _get_streak_display(self):
        """Get current streak display."""
        streak = st.session_state.current_streak
        if streak["count"] > 1:
            player_emoji = "🔵" if streak["player"] == "X" else "🔴"
            return f"<div style='color: #f5576c;'>🔥 Current Streak: {player_emoji} {streak['count']} wins!</div>"
        return ""

    def _render_leaderboard(self):
        """Render top performing models leaderboard."""
        st.markdown("### 🏆 TOP PERFORMERS")

        model_wins = st.session_state.session_stats["model_wins"]

        if model_wins:
            # Sort models by win count
            sorted_models = sorted(model_wins.items(), key=lambda x: x[1], reverse=True)[:3]

            medals = ["🥇", "🥈", "🥉"]
            for i, (model, wins) in enumerate(sorted_models):
                medal = medals[i] if i < len(medals) else "🏅"
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 10px;
                            border-radius: 8px; margin: 6px 0;'>
                    {medal} <strong>{model}</strong>: {wins} wins
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎮 Play some games to see top performers!")

    def _render_pro_tip(self):
        """Render a random pro tip."""
        import random

        tips = [
            "💡 Groq models respond lightning fast!",
            "💡 Larger models (70B) tend to play more strategically",
            "💡 Try mixing different providers for variety!",
            "💡 The center square is often the best opening move",
            "💡 8B models are faster but less strategic",
            "💡 Watch the move history to learn AI tactics",
            "💡 NVIDIA models offer great variety of sizes",
            "💡 Different models have unique playing styles",
        ]

        st.markdown("### 💡 PRO TIP")
        tip = random.choice(tips)
        st.markdown(f"""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 12px;
                    border-radius: 8px; border-left: 3px solid #667eea;'>
            {tip}
        </div>
        """, unsafe_allow_html=True)

    def render_game_area(self, selected_p_x: str, selected_p_o: str):
        """
        Render the main game area.

        Args:
            selected_p_x: Selected model for Player X
            selected_p_o: Selected model for Player O
        """
        if not st.session_state.game_started:
            st.info("👈 Press 'Start Game' to begin!")
            return

        # Show current matchup
        st.markdown(
            f"<h3 style='color:#87CEEB; text-align:center;'>{selected_p_x} vs {selected_p_o}</h3>",
            unsafe_allow_html=True,
        )

        # Get game state
        game_over, status = st.session_state.game_board.get_game_state()

        # Display board
        self.ui.display_board(st.session_state.game_board)

        # Show game status
        if game_over:
            self._display_game_over_status(status, selected_p_x, selected_p_o)
        else:
            # Show current player status
            current_player = st.session_state.game_board.current_player
            player_num = "1" if current_player == "X" else "2"
            current_model_name = selected_p_x if current_player == "X" else selected_p_o
            self.ui.show_agent_status(f"Player {player_num} ({current_model_name})", "It's your turn")

        # Display move history BEFORE processing next move
        self.ui.display_move_history()

        # Process agent move if game is active and not paused
        if not game_over and not st.session_state.game_paused:
            current_player = st.session_state.game_board.current_player
            player_num = "1" if current_player == "X" else "2"
            current_model_name = selected_p_x if current_player == "X" else selected_p_o
            self._process_agent_move(current_player, player_num, current_model_name)

    def _display_game_over_status(self, status: str, selected_p_x: str, selected_p_o: str):
        """Display game over status."""
        winner_player = "X" if "X wins" in status else "O" if "O wins" in status else None
        if winner_player:
            winner_model = selected_p_x if winner_player == "X" else selected_p_o
            streak_count = st.session_state.current_streak["count"]

            # Show celebration and victory banner
            st.balloons()
            self._show_victory_banner(winner_player, winner_model, streak_count)
            logger.info(f"Game Over - {status}")
        else:
            # Show the draw banner
            self._show_draw_banner()
            logger.info("Game Over - Draw")


    def _process_agent_move(self, current_player: str, player_num: str, current_model_name: str):
        """Process an agent's move."""
        # Show thinking indicator
        self.ui.show_thinking_indicator(player_num, current_model_name)

        valid_moves = st.session_state.game_board.get_valid_moves()
        current_agent = (
            st.session_state.player_x if current_player == "X" else st.session_state.player_o
        )

        try:
            # Get agent response
            response: RunOutput = current_agent.run(
                f"""\
Current board state:\n{st.session_state.game_board.get_board_state()}\n
Available valid moves (row, col): {valid_moves}\n
Choose your next move from the valid moves above.
Respond with ONLY two numbers for row and column, e.g. "1 2".""",
                stream=False,
            )

            # Parse and execute move
            numbers = re.findall(r"\d+", response.content if response else "")
            row, col = map(int, numbers[:2])
            success, message = st.session_state.game_board.make_move(row, col)

            if success:
                self._record_move(player_num, current_model_name, row, col)
                self._check_game_end()
                st.rerun()
            else:
                logger.error(f"Invalid move attempt: {message}")
                st.rerun()

        except Exception as e:
            logger.error(f"Error processing move: {str(e)}")
            st.error(f"Error processing move: {str(e)}")
            st.rerun()

    def _record_move(self, player_num: str, model_name: str, row: int, col: int):
        """Record a move in the history."""
        move_number = len(st.session_state.move_history) + 1
        st.session_state.move_history.append(
            {
                "number": move_number,
                "player": f"Player {player_num} ({model_name})",
                "move": f"{row},{col}",
            }
        )
        logger.info(f"Move {move_number}: Player {player_num} ({model_name}) -> ({row}, {col})")

    def _check_game_end(self):
        """Check if game has ended and update statistics."""
        game_over, status = st.session_state.game_board.get_game_state()
        if game_over:
            logger.info(f"Game ended: {status}")

            # Update statistics
            stats = st.session_state.session_stats
            stats["total_games"] += 1

            if "wins" in status:
                winner = "X" if "X wins" in status else "O"

                # Update win counters
                if winner == "X":
                    stats["x_wins"] += 1
                    winner_model = st.session_state.model_p1
                else:
                    stats["o_wins"] += 1
                    winner_model = st.session_state.model_p2

                # Track model performance for leaderboard
                if winner_model not in stats["model_wins"]:
                    stats["model_wins"][winner_model] = 0
                stats["model_wins"][winner_model] += 1

                # Update winning streak
                streak = st.session_state.current_streak
                if streak["player"] == winner:
                    streak["count"] += 1
                else:
                    streak["player"] = winner
                    streak["count"] = 1

                logger.info(f"Winner: {winner} ({winner_model}), Streak: {streak['count']}")
            else:
                stats["draws"] += 1
                st.session_state.current_streak = {"player": None, "count": 0}

            st.session_state.game_paused = True

    def _show_victory_banner(self, winner: str, winner_model: str, streak_count: int):
        """Display an exciting victory banner."""
        player_num = "1" if winner == "X" else "2"
        player_color = "#4facfe" if winner == "X" else "#f5576c"
        player_emoji = "🔵" if winner == "X" else "🔴"

        streak_html = ""
        if streak_count > 1:
            streak_html = f"""
            <div style='margin-top: 15px; font-size: 1.2em; animation: pulse 1.5s ease-in-out infinite;'>
                🔥 <strong>{streak_count} WIN STREAK!</strong> 🔥
            </div>
            """

        victory_html = f"""
        <style>
        @keyframes victoryPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        @keyframes slideDown {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        </style>
        <div style='background: linear-gradient(135deg, {player_color}22 0%, {player_color}44 100%);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border: 3px solid {player_color};
                    border-radius: 24px;
                    padding: 40px;
                    margin: 30px 0;
                    text-align: center;
                    box-shadow: 0 20px 60px {player_color}55, 0 0 40px {player_color}33;
                    animation: slideDown 0.6s ease-out, victoryPulse 2s ease-in-out infinite;'>
            <div style='font-size: 4em; margin-bottom: 10px;'>
                🏆
            </div>
            <div style='font-size: 2.5em; font-weight: 700;
                        background: linear-gradient(135deg, #fff 0%, {player_color} 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin-bottom: 15px;'>
                VICTORY!
            </div>
            <div style='font-size: 1.8em; margin-bottom: 10px;'>
                {player_emoji} <strong>PLAYER {player_num}</strong> {player_emoji}
            </div>
            <div style='font-size: 1.3em; color: #ddd; font-weight: 500;'>
                {winner_model}
            </div>
            {streak_html}
        </div>
        """
        st.markdown(victory_html, unsafe_allow_html=True)

    def _show_draw_banner(self):
        """Display a draw banner."""
        draw_html = """
        <style>
        @keyframes drawFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        </style>
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border: 3px solid #667eea;
                    border-radius: 24px;
                    padding: 40px;
                    margin: 30px 0;
                    text-align: center;
                    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
                    animation: drawFloat 3s ease-in-out infinite;'>
            <div style='font-size: 4em; margin-bottom: 10px;'>
                🤝
            </div>
            <div style='font-size: 2.5em; font-weight: 700;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin-bottom: 15px;'>
                IT'S A DRAW!
            </div>
            <div style='font-size: 1.3em; color: #ddd; font-weight: 500;'>
                Both AI agents played brilliantly!
            </div>
        </div>
        """
        st.markdown(draw_html, unsafe_allow_html=True)

    def run(self):
        """Run the main application."""
        self.configure_page()
        self.initialize_session_state()
        self.render_header()
        selected_p_x, selected_p_o, missing_keys = self.render_sidebar()
        self.render_game_area(selected_p_x, selected_p_o)


def main():
    """Application entry point."""
    logger.info("Starting Tic Tac Toe application")
    game = TicTacToeGame()
    game.run()


if __name__ == "__main__":
    main()
