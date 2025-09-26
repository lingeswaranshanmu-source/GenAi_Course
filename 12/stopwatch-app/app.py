# app.py
import streamlit as st
import time
from time import perf_counter
from datetime import datetime
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Stopwatch ⏱️", page_icon="⏱️", layout="centered")

# --- Helpers ---
def now_ms():
    """High-resolution current time in milliseconds."""
    return int(perf_counter() * 1000)

def format_time(ms: int) -> str:
    """Format milliseconds into HH:MM:SS.mmm (omit hours if zero)."""
    if ms < 0:
        ms = 0
    hours = ms // 3_600_000
    minutes = (ms % 3_600_000) // 60_000
    seconds = (ms % 60_000) // 1000
    millis = ms % 1000
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"
    return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

def ensure_state():
    """Initialize required session state keys."""
    if "running" not in st.session_state:
        st.session_state.running = False
    if "start_ts" not in st.session_state:
        st.session_state.start_ts = None   # perf_counter ms when started
    if "accum" not in st.session_state:
        st.session_state.accum = 0         # accumulated ms while paused
    if "laps" not in st.session_state:
        st.session_state.laps = []         # list of dicts {lap_no, time_ms, lap_ms, ts}
    if "last_display" not in st.session_state:
        st.session_state.last_display = "00:00.000"

ensure_state()

st.title("⏱️ Stopwatch")
st.write("Start / Stop / Reset. High-resolution timing using `perf_counter`. Lap support included.")

# layout: main display + controls + lap list
display_col, controls_col = st.columns([3, 1])

with display_col:
    st.subheader("Elapsed Time")
    timer_placeholder = st.empty()
    # compute current elapsed (ms)
    if st.session_state.running and st.session_state.start_ts is not None:
        elapsed = st.session_state.accum + (now_ms() - st.session_state.start_ts)
    else:
        elapsed = st.session_state.accum
    formatted = format_time(int(elapsed))
    st.session_state.last_display = formatted
    timer_placeholder.markdown(f"""<div style="font-size:48px; font-weight:700; font-family:monospace">{formatted}</div>""", unsafe_allow_html=True)

    st.markdown("---")
    # Laps
    st.subheader("Laps")
    if st.session_state.laps:
        laps_df = pd.DataFrame(st.session_state.laps)
        # Show lap number, lap time, cumulative time
        display_df = laps_df[["lap_no", "lap_time_str", "cum_time_str"]].rename(
            columns={"lap_no": "Lap", "lap_time_str": "Lap Time", "cum_time_str": "Elapsed"}
        )
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info("No laps recorded. Press 'Lap' while running to capture a split.")

with controls_col:
    st.subheader("Controls")
    # Start / Stop toggle
    if not st.session_state.running:
        if st.button("▶️ Start"):
            # start or resume
            st.session_state.start_ts = now_ms()
            st.session_state.running = True
            # immediate rerun to start update loop
            st.rerun()
    else:
        if st.button("⏸️ Stop"):
            # pause
            # accumulate time since start
            st.session_state.accum += now_ms() - st.session_state.start_ts
            st.session_state.start_ts = None
            st.session_state.running = False
            # keep display as-is (no rerun required)

    # Lap button
    lap_disabled = not st.session_state.running
    if st.button("🏁 Lap", disabled=lap_disabled):
        # capture elapsed
        if st.session_state.running:
            cum_ms = st.session_state.accum + (now_ms() - st.session_state.start_ts)
        else:
            cum_ms = st.session_state.accum
        last_cum = st.session_state.laps[-1]["time_ms"] if st.session_state.laps else 0
        lap_ms = cum_ms - last_cum
        lap_no = len(st.session_state.laps) + 1
        st.session_state.laps.append({
            "lap_no": lap_no,
            "time_ms": int(cum_ms),
            "lap_ms": int(lap_ms),
            "lap_time_str": format_time(int(lap_ms)),
            "cum_time_str": format_time(int(cum_ms)),
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # show success briefly then rerun to display updated laps
        st.success(f"Lap {lap_no} recorded: {format_time(int(lap_ms))}")
        st.rerun()

    # Reset button
    if st.button("🧹 Reset"):
        st.session_state.running = False
        st.session_state.start_ts = None
        st.session_state.accum = 0
        st.session_state.laps = []
        st.session_state.last_display = "00:00.000"
        # rerun to refresh UI
        st.rerun()

    st.markdown("---")
    st.markdown("**Precision**: updates every 100 ms")
    st.markdown("**Note**: Timer uses high-resolution clock; it remains accurate if tab backgrounded.")

# --- Export laps if any ---
if st.session_state.laps:
    df_laps = pd.DataFrame(st.session_state.laps)[["lap_no", "ts", "lap_time_str", "cum_time_str"]]
    df_laps = df_laps.rename(columns={"lap_no": "Lap", "ts": "Timestamp", "lap_time_str": "Lap Time", "cum_time_str": "Elapsed"})
    csv = df_laps.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Laps (CSV)", data=csv, file_name=f"stopwatch_laps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")

# --- Update loop: if running, sleep a short time and rerun to refresh display ---
if st.session_state.running:
    # sleep for smooth UI updates; this blocks current run briefly and triggers rerun
    time.sleep(0.1)   # 100 ms refresh target
    st.rerun()
