import pyautogui, time
print("Move mouse — press Ctrl+C to stop")
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}  Y: {y}", end="\r", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped.")

