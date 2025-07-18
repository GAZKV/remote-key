import sys
import ctypes
from ctypes import wintypes
from types import SimpleNamespace

_backend_name = 'pyautogui'
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
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    INPUT_MOUSE = 0
    INPUT_KEYBOARD = 1

    KEYEVENTF_KEYUP = 0x0002

    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040

    try:
        ULONG_PTR = wintypes.ULONG_PTR
    except AttributeError:
        ULONG_PTR = ctypes.c_ulong

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ('wVk', wintypes.WORD),
            ('wScan', wintypes.WORD),
            ('dwFlags', wintypes.DWORD),
            ('time', wintypes.DWORD),
            ('dwExtraInfo', ULONG_PTR),
        ]

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ('dx', wintypes.LONG),
            ('dy', wintypes.LONG),
            ('mouseData', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('time', wintypes.DWORD),
            ('dwExtraInfo', ULONG_PTR),
        ]

    class _INPUT_UNION(ctypes.Union):
        _fields_ = [('ki', KEYBDINPUT), ('mi', MOUSEINPUT)]

    class INPUT(ctypes.Structure):
        _anonymous_ = ('u',)
        _fields_ = [('type', wintypes.DWORD), ('u', _INPUT_UNION)]

    user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
    user32.SendInput.restype = wintypes.UINT

    def _send_input(inp):
        if user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT)) != 1:
            raise ctypes.WinError(ctypes.get_last_error())

    VK = {
        'ctrl': 0x11,
        'alt': 0x12,
        'shift': 0x10,
        'win': 0x5B,
        'enter': 0x0D,
        'tab': 0x09,
        'esc': 0x1B,
        'space': 0x20,
    }
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        VK[c.lower()] = ord(c)
    for n in range(10):
        VK[str(n)] = 0x30 + n
    for n in range(1, 13):
        VK[f'f{n}'] = 0x70 + n - 1

    def key_down(k: str) -> None:
        vk = VK.get(k.lower())
        if vk is None:
            raise ValueError(f'Unsupported key: {k}')
        inp = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=vk, dwFlags=0))
        _send_input(inp)

    def key_up(k: str) -> None:
        vk = VK.get(k.lower())
        if vk is None:
            raise ValueError(f'Unsupported key: {k}')
        inp = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=vk, dwFlags=KEYEVENTF_KEYUP))
        _send_input(inp)

    def press(k: str) -> None:
        key_down(k)
        key_up(k)

    def hotkey(*keys: str) -> None:
        for k in keys:
            key_down(k)
        for k in reversed(keys):
            key_up(k)

    def click(button: str = 'left') -> None:
        button = button.lower()
        mapping = {
            'left': (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
            'right': (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
            'middle': (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
        }
        events = mapping.get(button)
        if not events:
            raise ValueError(f'Unsupported mouse button: {button}')
        for flag in events:
            inp = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=flag))
            _send_input(inp)

    backend = SimpleNamespace(press=press, hotkey=hotkey, click=click)
    _backend_name = 'sendinput'
else:
    import pyautogui

    pyautogui.FAILSAFE = False
    backend = pyautogui
    _backend_name = 'pyautogui'

_MOUSE_MAP = {
    'left_click': 'left',
    'right_click': 'right',
    'middle_click': 'middle',
}

_NUMPAD_MAP = {f'numpad_{i}': f'num{i}' for i in range(10)}

def send_key_combo(combo: str) -> None:
    combo_lower = combo.lower()
    if combo_lower in _MOUSE_MAP:
        backend.click(button=_MOUSE_MAP[combo_lower])
        return

    keys = [_NUMPAD_MAP.get(k.lower(), k.lower()) for k in combo.split('+')]
    if len(keys) == 1:
        backend.press(keys[0])
    else:
        backend.hotkey(*keys)

def send_key_sequence(seq) -> None:
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

    import time
    import re

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'wait' and i + 1 < len(tokens):
            m = re.match(r'^(\d+)(?:ms)?$', tokens[i + 1])
            if m:
                time.sleep(int(m.group(1)) / 1000)
                i += 2
                continue
        m = re.match(r'^wait(\d+)(?:ms)?$', token)
        if m:
            time.sleep(int(m.group(1)) / 1000)
            i += 1
            continue

        send_key_combo(token)
        i += 1

BACKEND_NAME = _backend_name
PLATFORM = _platform
