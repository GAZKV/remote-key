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

# Mapea cada botón a una lista de secuencias de teclas
# Map each button to a list of key sequences
key_sequences = {
    '1': ['alt+n'],
    '2': ['alt+c'],
    '3': ['n'],
    '4': ['1'],
    '5': ['ctrl+a'],
    '6': ['ctrl+c'],
    '7': ['ctrl+v'],
    '8': ['f5'],
    '9': ['esc'],
    '10': ['enter'],
    '11': ['tab'],
    '12': ['space']
}

@app.route('/')
def index():
    # Pasa el mapping a la plantilla
    # Pass the mapping to the template
    return render_template('index.html', key_sequences=key_sequences)

@app.route('/press/<btn_id>', methods=['POST'])
def press(btn_id):
    seq = key_sequences.get(btn_id)
    if not seq:
        return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404

    # Envía la secuencia de teclas completa usando send_key_sequence
    # Send the entire key sequence using send_key_sequence
    send_key_sequence(" ".join(seq))
    return jsonify({'status': 'ok', 'pressed': seq})

if __name__ == '__main__':
    # Atención: es posible que necesites ejecutar con privilegios
    # en algunos sistemas para que el envío de teclas funcione correctamente.
    # Note: on some systems you may need elevated privileges for
    # pyautogui to send key events properly.
    app.run(host='0.0.0.0', port=8000)
