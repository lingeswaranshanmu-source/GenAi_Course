import pyautogui
import time
from datetime import datetime
from pathlib import Path

# --------------------
# Safety & settings
# --------------------
pyautogui.FAILSAFE = True        # Move mouse to top-left corner to abort instantly
pyautogui.PAUSE = 0.25           # small pause after each PyAutoGUI call (optional)
START_COUNTDOWN_SECONDS = 5      # seconds before the script starts (so you can prepare)
ACTION_INTERVAL = 10             # seconds BETWEEN actions as you requested

# --------------------
# Helper: save screenshot
# --------------------
def take_screenshot_and_save():
    """Take a screenshot of the current screen and save to Desktop with timestamp."""
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)  # ensure Desktop exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = desktop / f"screenshot_{timestamp}.png"
    print(f"[INFO] Taking screenshot and saving to: {filename}")
    image = pyautogui.screenshot()   # takes screenshot of the entire screen
    image.save(filename)
    print("[INFO] Screenshot saved.")
    return filename

# --------------------
# Main sequence
# --------------------
def main():
    try:
        print(f"[INFO] Script will start in {START_COUNTDOWN_SECONDS} seconds. MOVE mouse to top-left to abort.")
        for i in range(START_COUNTDOWN_SECONDS, 0, -1):
            print(f"Starting in {i}...", end="\r")
            time.sleep(1)
        print("\n[INFO] Starting actions now.")

        # 1) Screenshot
        screenshot_file = take_screenshot_and_save()

        # 2) Wait ACTION_INTERVAL
        print(f"[INFO] Waiting {ACTION_INTERVAL} seconds before clicking (1/3).")
        time.sleep(ACTION_INTERVAL)

        # 3) Click at (100, 100)
        x1, y1 = 100, 100
        print(f"[INFO] Clicking at ({x1}, {y1}).")
        pyautogui.click(x=x1, y=y1)   # single click

        # 4) Wait ACTION_INTERVAL
        print(f"[INFO] Waiting {ACTION_INTERVAL} seconds before double-clicking (2/3).")
        time.sleep(ACTION_INTERVAL)

        # 5) Double-click at (100, 100)
        print(f"[INFO] Double-clicking at ({x1}, {y1}).")
        pyautogui.doubleClick(x=x1, y=y1)

        # 6) Wait ACTION_INTERVAL
        print(f"[INFO] Waiting {ACTION_INTERVAL} seconds before right-clicking (3/3).")
        time.sleep(ACTION_INTERVAL)

        # 7) Right-click at (100, 200)
        x2, y2 = 100, 200
        print(f"[INFO] Right-clicking at ({x2}, {y2}).")
        pyautogui.rightClick(x=x2, y=y2)

        print("[INFO] Done. All actions completed successfully.")
        print(f"[INFO] Screenshot saved at: {screenshot_file}")

    except pyautogui.FailSafeException:
        print("\n[WARN] Aborted by moving mouse to top-left (FailSafe triggered).")
    except KeyboardInterrupt:
        print("\n[WARN] Aborted by Ctrl+C.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()