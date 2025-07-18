from flask import Flask, render_template, jsonify, request
import sys
import keyboard_backend as kb
import subprocess
import shlex
import re
import requests

app = Flask(__name__)


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
        'color': '#f8d7da',
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '2': {
        'label': 'Botón 2 / Button 2',
        'type': 'keys',
        'cmd': '',
        'seq': ['alt+c'],
        'image': None,
        'color': '#d1e7dd',
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '3': {
        'label': 'Botón 3 / Button 3',
        'type': 'keys',
        'cmd': '',
        'seq': ['n'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '4': {
        'label': 'Botón 4 / Button 4',
        'type': 'keys',
        'cmd': '',
        'seq': ['1'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '5': {
        'label': 'Botón 5 / Button 5',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+a'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '6': {
        'label': 'Botón 6 / Button 6',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+c'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '7': {
        'label': 'Botón 7 / Button 7',
        'type': 'keys',
        'cmd': '',
        'seq': ['ctrl+v'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '8': {
        'label': 'Botón 8 / Button 8',
        'type': 'keys',
        'cmd': '',
        'seq': ['f5'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '9': {
        'label': 'Botón 9 / Button 9',
        'type': 'keys',
        'cmd': '',
        'seq': ['esc'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '10': {
        'label': 'Botón 10 / Button 10',
        'type': 'keys',
        'cmd': '',
        'seq': ['enter'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '11': {
        'label': 'Botón 11 / Button 11',
        'type': 'keys',
        'cmd': '',
        'seq': ['tab'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
    },
    '12': {
        'label': 'Botón 12 / Button 12',
        'type': 'keys',
        'cmd': '',
        'seq': ['space'],
        'image': None,
        'color': None,
        'effect': 'anim',
        'sound': None,
        'method': 'GET',
        'url': '',
        'body': None
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
    if 'image' in data:
        btn['image'] = data.get('image')
    if 'color' in data:
        btn['color'] = data.get('color')
    if 'effect' in data:
        btn['effect'] = data.get('effect')
    if 'sound' in data:
        btn['sound'] = data.get('sound')
    if btn['type'] == 'shell':
        btn['cmd'] = str(data.get('cmd', '')).strip()
        return jsonify({'status': 'ok', 'type': 'shell', 'cmd': btn['cmd']})
    elif btn['type'] == 'http':
        btn['method'] = str(data.get('method', 'GET')).upper()
        btn['url'] = str(data.get('url', '')).strip()
        btn['body'] = data.get('body')
        return jsonify({
            'status': 'ok',
            'type': 'http',
            'method': btn['method'],
            'url': btn['url']
        })
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
    method_val = data.get('method') or request.values.get('method')
    url_val = data.get('url') or request.values.get('url')
    body_val = data.get('body') if 'body' in data else request.values.get('body')

    if btn_id in buttons:
        cfg = buttons[btn_id]
        action = req_type or cfg.get('type', 'keys')
        if action == 'shell':
            cmd = cmd_val if cmd_val not in (None, '') else cfg.get('cmd')
            if not cmd:
                return jsonify({'status': 'error', 'message': 'Comando vacío'}), 400
            result = run_shell_command(cmd)
            return jsonify({'status': 'ok', 'stdout': result.stdout})
        elif action == 'http':
            method = (method_val or cfg.get('method', 'GET')).upper()
            url = url_val if url_val not in (None, '') else cfg.get('url')
            body = body_val if body_val not in (None, '') else cfg.get('body')
            if not url:
                return jsonify({'status': 'error', 'message': 'URL vacía'}), 400
            try:
                resp = requests.request(method, url, json=body)
                return jsonify({'status': 'ok', 'status_code': resp.status_code})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            seq = seq_val if seq_val not in (None, '') else cfg.get('seq')
    else:
        if req_type == 'shell':
            if not cmd_val:
                return jsonify({'status': 'error', 'message': 'Comando vacío'}), 400
            result = run_shell_command(cmd_val)
            return jsonify({'status': 'ok', 'stdout': result.stdout})
        elif req_type == 'http':
            if not url_val:
                return jsonify({'status': 'error', 'message': 'URL vacía'}), 400
            try:
                resp = requests.request((method_val or 'GET').upper(), url_val, json=body_val)
                return jsonify({'status': 'ok', 'status_code': resp.status_code})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            if seq_val in (None, ''):
                return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404
            seq = seq_val

    kb.send_key_sequence(seq)
    pressed = seq if isinstance(seq, list) else str(seq).split()
    return jsonify({'status': 'ok', 'pressed': pressed})


@app.route('/export', methods=['GET'])
def export_config():
    """Return the current button configuration as JSON."""
    return jsonify(buttons)


@app.route('/import', methods=['POST'])
def import_config():
    """Import configuration from a JSON payload and update server state."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Invalid config'}), 400

    for btn_id, cfg in data.items():
        if not isinstance(cfg, dict):
            continue
        btn = buttons.setdefault(str(btn_id), {})
        for key in (
            'label',
            'type',
            'cmd',
            'seq',
            'image',
            'color',
            'effect',
            'sound',
            'method',
            'url',
            'body',
        ):
            if key in cfg:
                btn[key] = cfg[key]

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Atención: es posible que necesites ejecutar con privilegios
    # en algunos sistemas para que el envío de teclas funcione correctamente.
    # Note: on some systems you may need elevated privileges for
    # pyautogui to send key events properly.
    print(
        f"Detected platform: {kb.PLATFORM}. Using {kb.BACKEND_NAME} backend.",
        file=sys.stderr,
    )
    app.run(host='0.0.0.0', port=8000)
