import streamlit as st
import random

st.set_page_config(page_title="Tic-Tac-Toe ❌⭕", page_icon="❌⭕", layout="centered")

# ---------- Win combinations ----------
WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6]              # diagonals
]

# ---------- Session state initialization ----------
def ensure_state():
    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
    if "current_player" not in st.session_state:
        st.session_state.current_player = "X"  # X always starts
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "winning_line" not in st.session_state:
        st.session_state.winning_line = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "score_x" not in st.session_state:
        st.session_state.score_x = 0
    if "score_o" not in st.session_state:
        st.session_state.score_o = 0
    if "vs_computer" not in st.session_state:
        st.session_state.vs_computer = False

ensure_state()

# ---------- Helper functions ----------
def check_winner(board):
    for combo in WIN_COMBOS:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a], combo
    if "" not in board:
        return "Tie", []
    return None, []

def make_move(idx):
    """Attempt to place current player's mark at idx."""
    if st.session_state.game_over:
        return
    if st.session_state.board[idx] != "":
        return
    st.session_state.board[idx] = st.session_state.current_player
    # check for winner
    winner, combo = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.winning_line = combo
        st.session_state.game_over = True
        if winner == "X":
            st.session_state.score_x += 1
        elif winner == "O":
            # tie does not increment
            if winner == "Tie":
                pass
            else:
                st.session_state.score_o += 1
    else:
        # switch player
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

def computer_move_random():
    """Computer plays as 'O' - picks random empty square."""
    empties = [i for i, v in enumerate(st.session_state.board) if v == ""]
    if not empties or st.session_state.game_over:
        return
    choice = random.choice(empties)
    st.session_state.board[choice] = "O"
    winner, combo = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.winning_line = combo
        st.session_state.game_over = True
        if winner == "O":
            st.session_state.score_o += 1
    else:
        st.session_state.current_player = "X"

def new_game(clear_scores=False):
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.game_over = False
    if clear_scores:
        st.session_state.score_x = 0
        st.session_state.score_o = 0

# ---------- UI ----------
st.title("❌⭕ Tic-Tac-Toe")

# Sidebar controls: vs computer toggle, new game, reset scores
with st.sidebar:
    st.header("Options")
    vs_cpu = st.checkbox("Play vs Computer (random AI)", value=st.session_state.vs_computer)
    st.session_state.vs_computer = vs_cpu
    st.write("")  # spacer
    if st.button("🔁 New Game"):
        new_game(clear_scores=False)
    if st.button("🧾 Reset Scores"):
        new_game(clear_scores=True)

# Board rendering
st.subheader(f"Current: **{st.session_state.current_player}**" if not st.session_state.game_over else "Game Over")
cols = st.columns(3)
for i in range(9):
    col = cols[i % 3]
    # Determine button label and disabled status
    cell_value = st.session_state.board[i]
    is_winning_cell = i in st.session_state.winning_line
    if cell_value == "":
        # empty cell: clickable if game not over and if it's player's turn (if vs_computer controls who)
        disabled = st.session_state.game_over
        if col.button(" ", key=f"cell_{i}", disabled=disabled):
            if not st.session_state.game_over:
                # Make player's move only if it's human's turn
                # If vs_computer and current_player == 'O', disable human play (computer moves)
                if st.session_state.vs_computer and st.session_state.current_player == "O":
                    # ignore click — it's computer's turn
                    pass
                else:
                    make_move(i)
                    # if vs computer and now game not over and it's O's turn, let computer play
                    if st.session_state.vs_computer and not st.session_state.game_over and st.session_state.current_player == "O":
                        computer_move_random()
    else:
        # filled cell: render disabled button with label and highlight if winning
        label = cell_value
        if is_winning_cell:
            # visually highlight by adding emoji around symbol
            label = f"🎉 {cell_value} 🎉"
        col.button(label, key=f"cell_filled_{i}", disabled=True)

# Status and winner display
if st.session_state.game_over:
    if st.session_state.winner == "Tie":
        st.success("It's a Tie! 🤝")
    else:
        st.success(f"🎉 Winner: {st.session_state.winner}")
        # optional: show which line won
        st.info(f"Winning line: {st.session_state.winning_line}")
else:
    st.info("Game in progress. Click an empty cell to play.")

# Scoreboard
st.markdown("---")
st.subheader("Scoreboard")
c1, c2, c3 = st.columns(3)
c1.metric("Player X", st.session_state.score_x)
c2.metric("Player O", st.session_state.score_o)
c3.write("")  # spacer

# If vs_computer and it's computer's turn after rendering (e.g., page load), make computer move automatically
# (This handles the case where New Game left the turn on O — but normally X starts so safe).
if st.session_state.vs_computer and not st.session_state.game_over and st.session_state.current_player == "O":
    # make a computer move and rerun to update UI
    computer_move_random()
    st.experimental_rerun()  # one-time rerun to reflect computer move
