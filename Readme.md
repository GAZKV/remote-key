# Remote Key

A small Flask web application to trigger keyboard shortcuts from a browser.

## Installation

1. Ensure Python 3 is installed.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   On Windows you can run `install.cmd` instead, which performs the same installation step using the virtual environment's Python interpreter.
   Installing `pywin32` is optional; if it's missing, the backend provides fallback key codes so basic functionality still works.

## Running the server

Start the application with:
```bash
python app/app.py
```
The server listens on port **8000**. Open `http://localhost:8000` in your browser to access the control panel.

## Notes on privileges

The application relies on a small module (`keyboard_backend.py`) to send key events. It detects the host operating system when the server starts. `pyautogui` is used on all platforms, but on Windows key presses are sent using the native `SendInput` API directly. Installing `pywin32` is optional. Depending on your OS, sending key events may require administrator or root privileges. If you find that key presses are not working, try running the program with elevated permissions.

### OS support

* **Windows** – Works with `pyautogui`. Key events use the native `SendInput` API directly, so `pywin32` is optional.
* **Linux/macOS** – Uses `pyautogui`. On Linux you must also install `python3-xlib` (via pip or your package manager). On macOS `pyobjc` (or `pyobjc-core`/`pyobjc-framework-Quartz`) is needed so `pyautogui` can access the accessibility APIs.

On Linux, additional system packages like `python3-xlib` may be required for `pyautogui` to function correctly. macOS users should ensure the `pyobjc` dependencies are installed.

## Using the interface

The web page displays a grid of buttons. Each button corresponds to a sequence of keys defined in `app/app.py`. Clicking a button sends a request to the server, which then presses and releases the configured keys on the host machine.

### Multiple actions per button

You can configure a button to execute several key combinations in order. In the
configuration panel, enter one combination per line, for example:

```
ctrl+c
ctrl+v
```

The server will press `Ctrl+C` followed by `Ctrl+V`. The API also accepts JSON
arrays of actions:

```bash
curl -X POST http://localhost:8000/press/1 \
     -H 'Content-Type: application/json' \
     -d '{"seq": ["ctrl+c", "ctrl+v"]}'
```

## Troubleshooting

If a key press fails on Windows, the backend now raises an `OSError` with the
original Windows error code from `SendInput`. Checking this code can help you
identify permission or driver issues when events don't fire.
