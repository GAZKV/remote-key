# Remote Key

A small Flask web application to trigger keyboard shortcuts from a browser.

## Installation

1. Ensure Python 3 is installed.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   On Windows you can run `install.cmd` instead, which performs the same installation step using the virtual environment's Python interpreter.

## Running the server

Start the application with:
```bash
python app/app.py
```
The server listens on port **8000**. Open `http://localhost:8000` in your browser to access the control panel.

## Notes on privileges

The application relies on the [`keyboard`](https://pypi.org/project/keyboard/) library to emulate key presses. Depending on your operating system, sending key events may require administrator or root privileges. If you find that key presses are not working, try running the program with elevated permissions.

## Using the interface

The web page displays a grid of buttons. Each button corresponds to a sequence of keys defined in `app/app.py`. Clicking a button sends a request to the server, which then presses and releases the configured keys on the host machine.
