from flask import Flask, render_template, jsonify
import pyautogui

# Disable the fail-safe feature so moving the mouse to a corner
# doesn't raise an exception during automated key presses.
pyautogui.FAILSAFE = False

app = Flask(__name__)


def send_key_combo(combo: str) -> None:
    """Send a key combination using pyautogui.

    The incoming string uses the ``"ctrl+alt+del"`` style syntax. When
    multiple keys are separated by ``+`` they will be pressed
    simultaneously, otherwise a single key press is issued.
    """
    keys = combo.split("+")
    if len(keys) == 1:
        pyautogui.press(keys[0])
    else:
        pyautogui.hotkey(*keys)


def send_key_sequence(text: str) -> None:
    """Send a whitespace separated sequence of key combinations.

    Each segment in ``text`` represents a combination in ``ctrl+alt+del`` style
    syntax and will be executed in order.
    """
    text = text.strip()
    if not text:
        return

    for combo in text.split():
        send_key_combo(combo)

# Map each button to its configuration including
# the key sequence and an optional background image
buttons = {
    '1': {'seq': ['alt+n'], 'image': None, 'color': '#f8d7da'},
    '2': {'seq': ['alt+c'], 'image': None, 'color': '#d1e7dd'},
    '3': {'seq': ['n'], 'image': None, 'color': None},
    '4': {'seq': ['1'], 'image': None, 'color': None},
    '5': {'seq': ['ctrl+a'], 'image': None, 'color': None},
    '6': {'seq': ['ctrl+c'], 'image': None, 'color': None},
    '7': {'seq': ['ctrl+v'], 'image': None, 'color': None},
    '8': {'seq': ['f5'], 'image': None, 'color': None},
    '9': {'seq': ['esc'], 'image': None, 'color': None},
    '10': {'seq': ['enter'], 'image': None, 'color': None},
    '11': {'seq': ['tab'], 'image': None, 'color': None},
    '12': {'seq': ['space'], 'image': None, 'color': None}
}

@app.route('/')
def index():
    # Pass the button configuration to the template
    return render_template('index.html', buttons=buttons)

@app.route('/press/<btn_id>', methods=['POST'])
def press(btn_id):
    btn = buttons.get(btn_id)
    if not btn:
        return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404

    seq = btn['seq']
    # Send the entire key sequence using send_key_sequence
    send_key_sequence(" ".join(seq))
    return jsonify({'status': 'ok', 'pressed': seq})

if __name__ == '__main__':
    # Atención: es posible que necesites ejecutar con privilegios
    # en algunos sistemas para que el envío de teclas funcione correctamente.
    # Note: on some systems you may need elevated privileges for
    # pyautogui to send key events properly.
    app.run(host='0.0.0.0', port=8000)
