"""
CSS styles for the Tic Tac Toe application UI.
Modern Clean Design with Glass Morphism
"""

CUSTOM_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Root Variables */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    --player-x-color: #4facfe;
    --player-o-color: #f5576c;
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --shadow-soft: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    --shadow-glow: 0 0 20px rgba(79, 172, 254, 0.4);
}

/* Global Styles */
* {
    font-family: 'Poppins', sans-serif;
}

/* Main Title with Vibrant Gradient */
.main-title {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5em;
    font-weight: 700;
    padding: 0.5em 0;
    letter-spacing: -1px;
    animation: titleFloat 3s ease-in-out infinite;
    text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
}

@keyframes titleFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Game Board - Glass Morphism with Glow */
.game-board {
    display: grid;
    grid-template-columns: repeat(3, 120px);
    gap: 12px;
    justify-content: center;
    margin: 2em auto;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 24px;
    border: 1px solid var(--glass-border);
    box-shadow: var(--shadow-soft), var(--shadow-glow);
    width: fit-content;
    animation: boardEntrance 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes boardEntrance {
    from {
        opacity: 0;
        transform: scale(0.8) rotateX(10deg);
    }
    to {
        opacity: 1;
        transform: scale(1) rotateX(0deg);
    }
}

/* Board Cells - Animated with Glow */
.board-cell {
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5em;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    color: #fff;
    border-radius: 16px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.board-cell::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.board-cell:hover::before {
    opacity: 1;
}

.board-cell:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4),
                0 0 40px rgba(79, 172, 254, 0.3);
    border-color: rgba(79, 172, 254, 0.6);
}

/* X and O Styling with Gradients */
.board-cell:contains("X") {
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
    color: var(--player-x-color);
    text-shadow: 0 0 20px rgba(79, 172, 254, 0.8);
    animation: pieceAppear 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.board-cell:contains("O") {
    background: linear-gradient(135deg, rgba(245, 87, 108, 0.2) 0%, rgba(250, 112, 154, 0.2) 100%);
    color: var(--player-o-color);
    text-shadow: 0 0 20px rgba(245, 87, 108, 0.8);
    animation: pieceAppear 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes pieceAppear {
    0% {
        opacity: 0;
        transform: scale(0) rotate(180deg);
    }
    60% {
        transform: scale(1.2) rotate(-10deg);
    }
    100% {
        opacity: 1;
        transform: scale(1) rotate(0deg);
    }
}

/* Agent Status - Glass Card */
.agent-status {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-left: 4px solid var(--player-x-color);
    padding: 16px 24px;
    margin: 20px auto;
    border-radius: 16px;
    max-width: 600px;
    text-align: center;
    box-shadow: var(--shadow-soft);
    animation: statusSlide 0.4s ease-out;
    font-weight: 500;
}

@keyframes statusSlide {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Thinking Indicator - Animated Pulse */
.thinking-container {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    min-width: 350px;
}

.agent-thinking {
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 16px 24px;
    border-radius: 50px;
    border: 2px solid rgba(250, 112, 154, 0.5);
    box-shadow: 0 8px 32px rgba(250, 112, 154, 0.3),
                0 0 60px rgba(250, 112, 154, 0.2);
    animation: thinkingPulse 2s ease-in-out infinite;
}

@keyframes thinkingPulse {
    0%, 100% {
        box-shadow: 0 8px 32px rgba(250, 112, 154, 0.3),
                    0 0 40px rgba(250, 112, 154, 0.2);
    }
    50% {
        box-shadow: 0 8px 32px rgba(250, 112, 154, 0.5),
                    0 0 80px rgba(250, 112, 154, 0.4);
    }
}

.agent-thinking > div:first-child {
    animation: rotate 2s linear infinite;
    margin-right: 12px;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Move History - Card Based Design */
.history-header {
    text-align: center;
    margin-bottom: 30px;
    font-size: 1.8em;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.history-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    width: 100%;
    margin: 0;
    padding: 0;
}

.history-column-left,
.history-column-right {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin: 0;
    padding: 0;
    width: 100%;
}

/* Move Entry - Professional Cards */
.move-entry {
    display: flex;
    align-items: center;
    padding: 16px;
    margin: 10px 0;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid var(--glass-border);
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation: cardSlideIn 0.4s ease-out;
}

@keyframes cardSlideIn {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.move-entry:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.move-entry.player1 {
    border-left: 4px solid var(--player-x-color);
    box-shadow: 0 4px 16px rgba(79, 172, 254, 0.2);
}

.move-entry.player1:hover {
    box-shadow: 0 8px 24px rgba(79, 172, 254, 0.3);
}

.move-entry.player2 {
    border-left: 4px solid var(--player-o-color);
    box-shadow: 0 4px 16px rgba(245, 87, 108, 0.2);
}

.move-entry.player2:hover {
    box-shadow: 0 8px 24px rgba(245, 87, 108, 0.3);
}

/* Mini Board - Enhanced */
.mini-board {
    display: grid;
    grid-template-columns: repeat(3, 28px);
    gap: 3px;
    background: rgba(255, 255, 255, 0.05);
    padding: 4px;
    border-radius: 8px;
    margin-right: 16px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
}

.mini-cell {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.03);
    color: #fff;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.mini-cell.highlight.player1 {
    background: linear-gradient(135deg, var(--player-x-color) 0%, #00f2fe 100%);
    color: white;
    box-shadow: 0 0 12px rgba(79, 172, 254, 0.6);
    animation: cellPulse 0.5s ease;
}

.mini-cell.highlight.player2 {
    background: linear-gradient(135deg, var(--player-o-color) 0%, #fa709a 100%);
    color: white;
    box-shadow: 0 0 12px rgba(245, 87, 108, 0.6);
    animation: cellPulse 0.5s ease;
}

@keyframes cellPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Move Info */
.move-info {
    flex-grow: 1;
    padding-left: 12px;
}

.move-number {
    font-weight: 700;
    font-size: 1.1em;
    margin-right: 10px;
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.1);
}

.move-number.player1 {
    color: var(--player-x-color);
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
}

.move-number.player2 {
    color: var(--player-o-color);
    background: linear-gradient(135deg, rgba(245, 87, 108, 0.2) 0%, rgba(250, 112, 154, 0.2) 100%);
}

/* Win Celebration Animation */
@keyframes confetti {
    0% {
        transform: translateY(-100vh) rotate(0deg);
        opacity: 1;
    }
    100% {
        transform: translateY(100vh) rotate(720deg);
        opacity: 0;
    }
}

.celebration {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 9999;
}

.confetti-piece {
    position: absolute;
    width: 10px;
    height: 10px;
    background: var(--player-x-color);
    animation: confetti 3s ease-out forwards;
}

/* Smooth Transitions for All Elements */
* {
    transition: background-color 0.3s ease,
                color 0.3s ease,
                border-color 0.3s ease;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Streamlit Button Styling */
.stButton > button {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: white;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 1em;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    width: 100%;
    white-space: nowrap;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    border-color: rgba(102, 126, 234, 0.6);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
}

.stButton > button:active {
    transform: translateY(0px);
}

.stButton > button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Streamlit Selectbox Styling */
.stSelectbox > div > div {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
    .game-board {
        grid-template-columns: repeat(3, 90px);
        gap: 8px;
        padding: 15px;
    }

    .board-cell {
        width: 90px;
        height: 90px;
        font-size: 2.5em;
    }

    .main-title {
        font-size: 2.5em;
    }

    .history-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .stButton > button {
        font-size: 0.9em;
        padding: 10px 16px;
    }
}
</style>
"""
