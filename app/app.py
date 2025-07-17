from flask import Flask, render_template, jsonify
import keyboard

app = Flask(__name__)

# Mapea cada botón a una lista de secuencias de teclas
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
    return render_template('index.html', key_sequences=key_sequences)

@app.route('/press/<btn_id>', methods=['POST'])
def press(btn_id):
    seq = key_sequences.get(btn_id)
    if not seq:
        return jsonify({'status': 'error', 'message': 'Botón no definido'}), 404

    # Ejecuta cada combinación de teclas
    for combo in seq:
        keyboard.press_and_release(combo)
    return jsonify({'status': 'ok', 'pressed': seq})

if __name__ == '__main__':
    # Atención: es necesario ejecutar con privilegios en algunos sistemas
    # para que keyboard funcione correctamente.
    app.run(host='0.0.0.0', port=8000)
