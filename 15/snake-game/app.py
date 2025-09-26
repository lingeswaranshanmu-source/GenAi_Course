# app.py
import streamlit as st
import random
import time

st.set_page_config(page_title="Snake Game 🐍", page_icon="🐍", layout="centered")

# -----------------
# Game Config
# -----------------
BOARD_SIZE = 20
TICK_RATE = 0.18  # seconds between moves (approx 180ms)

# -----------------
# Helpers
# -----------------
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

def init_game():
    st.session_state.snake = [(10, 10)]                    # head-first (row, col)
    st.session_state.direction = "RIGHT"
    st.session_state.food = random_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_move_time = time.time()
    st.session_state.paused = False

def random_food():
    while True:
        r = random.randint(0, BOARD_SIZE - 1)
        c = random.randint(0, BOARD_SIZE - 1)
        if (r, c) not in st.session_state.snake:
            return (r, c)

def direction_delta(direction):
    return {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
    }[direction]

def set_direction(new_dir):
    """Set direction unless it's a direct reverse of current direction."""
    if st.session_state.game_over:
        return
    cur = st.session_state.direction
    # Prevent reversing direction into itself (unless snake length == 1 you could allow; keep prevention)
    if OPPOSITE.get(new_dir) == cur:
        return
    st.session_state.direction = new_dir

def move_snake():
    head = st.session_state.snake[0]
    dx, dy = direction_delta(st.session_state.direction)
    new_head = (head[0] + dx, head[1] + dy)

    # Check collisions with walls
    if new_head[0] < 0 or new_head[0] >= BOARD_SIZE or new_head[1] < 0 or new_head[1] >= BOARD_SIZE:
        st.session_state.game_over = True
        return

    # Check collisions with self
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    # Move head
    st.session_state.snake.insert(0, new_head)

    # Check food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = random_food()
        # grow (don't pop tail)
    else:
        # normal move: pop tail
        st.session_state.snake.pop()

def render_board_markdown():
    """Return a markdown-friendly string showing the board with emojis."""
    empty = "⬛"
    head_emoji = "🟢"
    body_emoji = "🟩"
    food_emoji = "🍎"

    # build empty board
    board = [[empty for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # place food
    fr, fc = st.session_state.food
    board[fr][fc] = food_emoji
    # place snake (head first)
    for i, (r, c) in enumerate(st.session_state.snake):
        board[r][c] = head_emoji if i == 0 else body_emoji

    # join rows with no spaces to keep compact monospace block
    rows = ["".join(row) for row in board]
    return "```\n" + "\n".join(rows) + "\n```"

# -----------------
# Initialize Session State
# -----------------
if "snake" not in st.session_state:
    init_game()

# -----------------
# UI
# -----------------
st.title("🐍 Snake Game")
st.markdown(f"**Score:** {st.session_state.score}")

if st.session_state.game_over:
    st.error("💀 Game Over! Click Restart to play again.")
    if st.button("Restart"):
        init_game()
    st.stop()

# Controls layout (clear, consistent)
up_col, _, _ = st.columns([1, 0.2, 1])
with up_col:
    st.button("⬆️", key="btn_up", on_click=set_direction, args=("UP",))

mid_left, mid_center, mid_right = st.columns([1, 1, 1])
with mid_left:
    st.button("⬅️", key="btn_left", on_click=set_direction, args=("LEFT",))
with mid_center:
    # Pause / Resume toggle
    if st.session_state.paused:
        if st.button("▶️ Resume"):
            st.session_state.paused = False
            st.session_state.last_move_time = time.time()
            st.rerun()
    else:
        if st.button("⏸️ Pause"):
            st.session_state.paused = True
with mid_right:
    st.button("➡️", key="btn_right", on_click=set_direction, args=("RIGHT",))

down_col, _, _ = st.columns([1, 0.2, 1])
with down_col:
    st.button("⬇️", key="btn_down", on_click=set_direction, args=("DOWN",))

st.markdown("---")

# -----------------
# Game Tick Loop
# -----------------
now = time.time()
if not st.session_state.paused and not st.session_state.game_over and (now - st.session_state.last_move_time) >= TICK_RATE:
    move_snake()
    st.session_state.last_move_time = now
    # rerun to refresh view for next tick
    st.rerun()

# Render board after potential move
st.markdown(render_board_markdown())

# -----------------
# Footer: status
# -----------------
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    st.write(f"Direction: **{st.session_state.direction}**")
with col2:
    st.write(f"Snake length: **{len(st.session_state.snake)}**")
