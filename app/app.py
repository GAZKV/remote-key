from flask import Flask, render_template, jsonify, request
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
# the key sequence, optional background image and
# a customizable label to display on the UI
buttons = {
    '1': {
        'label': 'Botón 1 / Button 1',
        'seq': ['alt+n'],
        'image': None,
        'color': '#f8d7da'
    },
    '2': {
        'label': 'Botón 2 / Button 2',
        'seq': ['alt+c'],
        'image': None,
        'color': '#d1e7dd'
    },
    '3': {
        'label': 'Botón 3 / Button 3',
        'seq': ['n'],
        'image': None,
        'color': None
    },
    '4': {
        'label': 'Botón 4 / Button 4',
        'seq': ['1'],
        'image': None,
        'color': None
    },
    '5': {
        'label': 'Botón 5 / Button 5',
        'seq': ['ctrl+a'],
        'image': None,
        'color': None
    },
    '6': {
        'label': 'Botón 6 / Button 6',
        'seq': ['ctrl+c'],
        'image': None,
        'color': None
    },
    '7': {
        'label': 'Botón 7 / Button 7',
        'seq': ['ctrl+v'],
        'image': None,
        'color': None
    },
    '8': {
        'label': 'Botón 8 / Button 8',
        'seq': ['f5'],
        'image': None,
        'color': None
    },
    '9': {
        'label': 'Botón 9 / Button 9',
        'seq': ['esc'],
        'image': None,
        'color': None
    },
    '10': {
        'label': 'Botón 10 / Button 10',
        'seq': ['enter'],
        'image': None,
        'color': None
    },
    '11': {
        'label': 'Botón 11 / Button 11',
        'seq': ['tab'],
        'image': None,
        'color': None
    },
    '12': {
        'label': 'Botón 12 / Button 12',
        'seq': ['space'],
        'image': None,
        'color': None
    }
}

@app.route('/')
def index():
    # Pass the button configuration to the template
    return render_template('index.html', buttons=buttons)


@app.route('/config/<btn_id>', methods=['POST'])
def update_config(btn_id):
    """Update the key sequence for a button."""
    btn = buttons.get(btn_id)
    if not btn:
        return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404

    data = request.get_json(silent=True) or {}
    seq_text = data.get('seq', '')
    btn['seq'] = seq_text.split() if seq_text else []
    return jsonify({'status': 'ok', 'seq': btn['seq']})

@app.route('/press/<btn_id>', methods=['POST'])
def press(btn_id):
    """Handle a press request for ``btn_id``.

    If ``btn_id`` exists in the ``buttons`` dictionary we fall back to its
    stored sequence when the incoming payload does not include ``seq``.  For
    dynamically created buttons that only exist on the client, the request will
    provide the sequence directly, so we simply execute it.
    """

    data = request.get_json(silent=True)
    if data and 'seq' in data:
        seq_text = data.get('seq', '')
    else:
        seq_text = request.values.get('seq', '')

    if btn_id in buttons:
        seq = seq_text.split() if seq_text else buttons[btn_id]['seq']
    else:
        if not seq_text:
            return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404
        seq = seq_text.split()

    send_key_sequence(" ".join(seq))
    return jsonify({'status': 'ok', 'pressed': seq})

if __name__ == '__main__':
    # Atención: es posible que necesites ejecutar con privilegios
    # en algunos sistemas para que el envío de teclas funcione correctamente.
    # Note: on some systems you may need elevated privileges for
    # pyautogui to send key events properly.
    app.run(host='0.0.0.0', port=8000)
