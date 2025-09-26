# Quiz Game App ❓ (Streamlit)

Simple quiz game built with Streamlit:
- Hardcoded multiple-choice questions
- Questions and options are shuffled
- Score tracked in `st.session_state`
- Final review + CSV export

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
streamlit run app.py

---

# 6) How it behaves / notes
- Questions and options are shuffled when the quiz is (re)started via **Restart with settings** in the sidebar or when Reset is clicked.  
- Session-state keys: `quiz`, `current_q`, `score`, `answers`, `finished`, `shuffle_questions`, `shuffle_options`.  
- You can go back one question with **Previous** — this will remove the last stored answer and adjust the score accordingly. (This is a simple, practical pattern.)  
- Final screen shows a review table and provides a CSV export of answers.

---

# 7) Step-by-step (copy/paste friendly)

1. Create project folder and files exactly as above.

2. Create and activate venv:
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - Mac/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
