# Snake Game 🐍 (Streamlit)

Classic Snake game built with Streamlit.

## Features
- 20x20 grid
- Snake moves automatically
- Control with Up/Down/Left/Right buttons
- Food spawns randomly
- Score increases when snake eats food
- Collision with walls or itself ends game
- Restart button to play again

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# or: source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
