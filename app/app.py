from flask import Flask, render_template, jsonify, request
import pyautogui
import subprocess
import shlex
import re

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


def send_key_sequence(seq) -> None:
    """Send a sequence of key combinations.

    ``seq`` can be either a whitespace separated string or a list of
    strings. In string form, any whitespace (spaces, newlines) is treated
    as a separator. Each resulting token must use the ``"ctrl+alt+del"``
    syntax, where ``+`` denotes simultaneous key presses. Tokens of the
    form ``wait <ms>`` (optionally written ``wait100`` or ``wait100ms``)
    insert a pause of the specified milliseconds between key combos.
    """

    if isinstance(seq, str):
        text = seq.strip()
        if not text:
            return
        tokens = text.split()
    elif isinstance(seq, list):
        tokens = [str(c).strip() for c in seq if str(c).strip()]
        if not tokens:
            return
    else:
        return

    import re
    import time

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Pattern: "wait", optional next token with numbers, or
        # forms like "wait100" or "wait100ms"
        if token == "wait" and i + 1 < len(tokens):
            m = re.match(r"^(\d+)(?:ms)?$", tokens[i + 1])
            if m:
                time.sleep(int(m.group(1)) / 1000)
                i += 2
                continue
        m = re.match(r"^wait(\d+)(?:ms)?$", token)
        if m:
            time.sleep(int(m.group(1)) / 1000)
            i += 1
            continue

        send_key_combo(token)
        i += 1


SAFE_CMD = re.compile(r'^[\w\-./ ]+$')


def run_shell_command(cmd: str):
    """Run a shell command safely with basic validation."""
    if not isinstance(cmd, str) or not SAFE_CMD.fullmatch(cmd.strip()):
        raise ValueError('Unsafe command')
    return subprocess.run(shlex.split(cmd), capture_output=True, text=True)

# Map each button to its configuration including
# the key sequence, optional background image and
# a customizable label to display on the UI
buttons = {
    '1': {
        'label': 'Botón 1 / Button 1',
        'type': 'keys',
        'cmd': '',
        'seq': ['alt+n'],
        'image': None,
        'color': '#f8d7da'
    },
    '2': {
        'label': 'Botón 2 / Button 2',
        'type': 'keys',
        'cmd': '',
        'seq': ['alt+c'],
        'image': None,
        'color': '#d1e7dd'
    },
    '3': {
        'label': 'Botón 3 / Button 3',
        'type': 'keys',
        'cmd': '',
        'seq': ['n'],
        'image': None,
        'color': None
    },
    '4': {
        'label': 'Botón 4 / Button 4',
        'type': 'keys',
        'cmd': '',
        'seq': ['1'],
        'image': None,
        'color': None
    },
    '5': {
        'label': 'Botón 5 / Button 5',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+a'],
        'image': None,
        'color': None
    },
    '6': {
        'label': 'Botón 6 / Button 6',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+c'],
        'image': None,
        'color': None
    },
    '7': {
        'label': 'Botón 7 / Button 7',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+v'],
        'image': None,
        'color': None
    },
    '8': {
        'label': 'Botón 8 / Button 8',
        'type': 'keys',
        'cmd': '',
        'seq': ['f5'],
        'image': None,
        'color': None
    },
    '9': {
        'label': 'Botón 9 / Button 9',
        'type': 'keys',
        'cmd': '',
        'seq': ['esc'],
        'image': None,
        'color': None
    },
    '10': {
        'label': 'Botón 10 / Button 10',
        'type': 'keys',
        'cmd': '',
        'seq': ['enter'],
        'image': None,
        'color': None
    },
    '11': {
        'label': 'Botón 11 / Button 11',
        'type': 'keys',
        'cmd': '',
        'seq': ['tab'],
        'image': None,
        'color': None
    },
    '12': {
        'label': 'Botón 12 / Button 12',
        'type': 'keys',
        'cmd': '',
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
    """Update the configuration for a button."""
    btn = buttons.get(btn_id)
    if not btn:
        return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404

    data = request.get_json(silent=True) or {}
    btn['type'] = data.get('type', btn.get('type', 'keys'))
    if btn['type'] == 'shell':
        btn['cmd'] = str(data.get('cmd', '')).strip()
        return jsonify({'status': 'ok', 'type': 'shell', 'cmd': btn['cmd']})
    else:
        seq_val = data.get('seq', '')
        if isinstance(seq_val, list):
            btn['seq'] = [str(s).strip() for s in seq_val if str(s).strip()]
        else:
            seq_text = str(seq_val)
            btn['seq'] = seq_text.split() if seq_text.strip() else []
        return jsonify({'status': 'ok', 'type': 'keys', 'seq': btn['seq']})

@app.route('/press/<btn_id>', methods=['POST'])
def press(btn_id):
    """Handle a press request for ``btn_id``.

    If ``btn_id`` exists in the ``buttons`` dictionary we fall back to its
    stored sequence when the incoming payload does not include ``seq``.  For
    dynamically created buttons that only exist on the client, the request will
    provide the sequence directly, so we simply execute it.
    """

    data = request.get_json(silent=True) or {}
    req_type = data.get('type') or request.values.get('type') or 'keys'
    cmd_val = data.get('cmd') or request.values.get('cmd')
    seq_val = data.get('seq') if 'seq' in data else request.values.get('seq')

    if btn_id in buttons:
        cfg = buttons[btn_id]
        action = req_type or cfg.get('type', 'keys')
        if action == 'shell':
            cmd = cmd_val if cmd_val not in (None, '') else cfg.get('cmd')
            if not cmd:
                return jsonify({'status': 'error', 'message': 'Comando vacío'}), 400
            result = run_shell_command(cmd)
            return jsonify({'status': 'ok', 'stdout': result.stdout})
        else:
            seq = seq_val if seq_val not in (None, '') else cfg.get('seq')
    else:
        if req_type == 'shell':
            if not cmd_val:
                return jsonify({'status': 'error', 'message': 'Comando vacío'}), 400
            result = run_shell_command(cmd_val)
            return jsonify({'status': 'ok', 'stdout': result.stdout})
        else:
            if seq_val in (None, ''):
                return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404
            seq = seq_val

    send_key_sequence(seq)
    pressed = seq if isinstance(seq, list) else str(seq).split()
    return jsonify({'status': 'ok', 'pressed': pressed})

if __name__ == '__main__':
    # Atención: es posible que necesites ejecutar con privilegios
    # en algunos sistemas para que el envío de teclas funcione correctamente.
    # Note: on some systems you may need elevated privileges for
    # pyautogui to send key events properly.
    app.run(host='0.0.0.0', port=8000)
