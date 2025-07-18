import sys
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

try:
    if _platform.startswith('win'):
        import win32api
        import win32con
        # Map basic keys to Virtual-Key codes
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
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            VK[c.lower()] = getattr(win32con, f'VK_{c}')
        for n in range(10):
            VK[str(n)] = getattr(win32con, f'VK_{n}')
        for n in range(1, 13):
            VK[f'f{n}'] = getattr(win32con, f'VK_F{n}')

        def key_down(k):
            vk = VK.get(k.lower())
            if vk is None:
                raise ValueError(f'Unsupported key: {k}')
            win32api.keybd_event(vk, 0, 0, 0)

        def key_up(k):
            vk = VK.get(k.lower())
            if vk is None:
                raise ValueError(f'Unsupported key: {k}')
            win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

        def press(k):
            key_down(k)
            key_up(k)

        def hotkey(*keys):
            for k in keys:
                key_down(k)
            for k in reversed(keys):
                key_up(k)

        backend = SimpleNamespace(press=press, hotkey=hotkey)
        _backend_name = 'pywin32'
    else:
        raise ImportError
except Exception:
    try:
        import pyautogui
    except Exception as exc:
        raise ImportError(
            'pyautogui is required on non-Windows platforms. ' \
            'Install python3-Xlib on Linux or pyobjc on macOS.'
        ) from exc
    pyautogui.FAILSAFE = False
    backend = pyautogui
    _backend_name = 'pyautogui'


def send_key_combo(combo: str) -> None:
    keys = combo.split('+')
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
