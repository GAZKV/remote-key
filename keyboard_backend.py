import sys
import ctypes
from types import SimpleNamespace

_backend_name = 'sendinput'
_platform_raw = sys.platform
if _platform_raw.startswith('win'):
    _platform = 'windows'
elif _platform_raw.startswith('linux'):
    _platform = 'linux'
elif _platform_raw == 'darwin':
    _platform = 'darwin'
else:
    _platform = _platform_raw

if _platform == 'windows':
    try:
        import win32con
    except ImportError:  # pragma: no cover - simplified constants for tests
        class win32con:  # type: ignore
            VK_CONTROL = 0x11
            VK_MENU = 0x12
            VK_SHIFT = 0x10
            VK_LWIN = 0x5B
            VK_RETURN = 0x0D
            VK_TAB = 0x09
            VK_ESCAPE = 0x1B
            VK_SPACE = 0x20
            VK_NUMPAD0 = 0x60
            for _i in range(1, 10):
                locals()[f'VK_NUMPAD{_i}'] = 0x60 + _i
            for _i in range(1, 13):
                locals()[f'VK_F{_i}'] = 0x70 + (_i - 1)

    # Mapeo de teclas virtuales (VK codes)
    VK = {
        'ctrl': win32con.VK_CONTROL,
        'alt': win32con.VK_MENU,
        'shift': win32con.VK_SHIFT,
        'win': win32con.VK_LWIN,
        'enter': win32con.VK_RETURN,
        'tab': win32con.VK_TAB,
        'esc': win32con.VK_ESCAPE,
        'space': win32con.VK_SPACE,
    }
    # Letras A-Z
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        VK[c.lower()] = ord(c)
    # Numeros fila superior 0-9
    for n in range(10):
        VK[str(n)] = ord(str(n))
    # Numpad 0-9
    VK['numpad_0'] = win32con.VK_NUMPAD0
    for i in range(1, 10):
        VK[f'numpad_{i}'] = win32con.VK_NUMPAD0 + i
    # Funcion F1-F12
    for n in range(1, 13):
        VK[f'f{n}'] = getattr(win32con, f'VK_F{n}')

    # Constantes SendInput
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", ctypes.c_ushort),
            ("wScan", ctypes.c_ushort),
            ("dwFlags", ctypes.c_ulong),
            ("time", ctypes.c_ulong),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", ctypes.c_long),
            ("dy", ctypes.c_long),
            ("mouseData", ctypes.c_ulong),
            ("dwFlags", ctypes.c_ulong),
            ("time", ctypes.c_ulong),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT), ("mi", MOUSEINPUT)]
        _anonymous_ = ("_input",)
        _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]

    SendInput = ctypes.WinDLL('user32', use_last_error=True).SendInput

    def _send_input_keyboard(vk, flags=0):
        extra = ctypes.c_ulong(0)
        ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=flags, time=0, dwExtraInfo=ctypes.pointer(extra))
        inp = INPUT(type=INPUT_KEYBOARD, ki=ki)
        if SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp)) == 0:
            code = ctypes.get_last_error()
            raise ctypes.WinError(code)

    def key_down(k: str) -> None:
        vk = VK.get(k.lower())
        if vk is None:
            raise ValueError(f'Unsupported key: {k}')
        _send_input_keyboard(vk, 0)

    def key_up(k: str) -> None:
        vk = VK.get(k.lower())
        if vk is None:
            raise ValueError(f'Unsupported key: {k}')
        _send_input_keyboard(vk, KEYEVENTF_KEYUP)

    def press(k: str) -> None:
        key_down(k)
        key_up(k)

    def hotkey(*keys: str) -> None:
        for k in keys:
            key_down(k)
        for k in reversed(keys):
            key_up(k)

    def click(button='left') -> None:
        extra = ctypes.c_ulong(0)
        down_flags = {'left':0x0002,'right':0x0008,'middle':0x0020}
        up_flags = {'left':0x0004,'right':0x0010,'middle':0x0040}
        btn = button.lower()
        if btn not in down_flags:
            raise ValueError(f'Unsupported mouse button: {button}')
        for flag in (down_flags[btn], up_flags[btn]):
            mi = MOUSEINPUT(0,0,0,flag,0,ctypes.pointer(extra))
            inp = INPUT(type=INPUT_KEYBOARD, mi=mi)
            SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

    backend = SimpleNamespace(press=press, hotkey=hotkey, click=click)
else:
    import pyautogui
    pyautogui.FAILSAFE = False
    backend = pyautogui
    _backend_name = 'pyautogui'

# Comandos especiales soportados
_SPECIAL_COMMANDS = {
    'left_click': 'left',
    'right_click': 'right',
    'middle_click': 'middle',
    **{f'numpad_{i}': f'num{i}' for i in range(10)},
}

def send_key_combo(combo: str):
    combo_lower = combo.lower()
    if combo_lower in _SPECIAL_COMMANDS and 'click' in combo_lower:
        backend.click(button=_SPECIAL_COMMANDS[combo_lower])
        return

    parts = [
        _SPECIAL_COMMANDS.get(p.lower(), p.lower())
        for p in combo.split('+')
    ]

    if len(parts) == 1:
        backend.press(parts[0])
    else:
        backend.hotkey(*parts)

def send_key_sequence(seq):
    import time, re
    tokens = []
    if isinstance(seq, str):
        tokens = seq.strip().split()
    elif isinstance(seq, list):
        tokens = [str(t).strip() for t in seq if str(t).strip()]

    # Preprocess tokens to merge "wait" with an immediately following integer
    merged = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'wait' and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            m = re.match(r'^(\d+)(?:ms)?$', nxt)
            if m:
                merged.append(f"wait{m.group(1)}")
                i += 2
                continue
        merged.append(token)
        i += 1

    i = 0
    while i < len(merged):
        token = merged[i]
        m = re.match(r'^wait(\d+)(?:ms)?$', token)
        if m:
            time.sleep(int(m.group(1)) / 1000.0)
        else:
            send_key_combo(token)
        i += 1

BACKEND_NAME = _backend_name
PLATFORM = _platform
