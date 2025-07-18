import importlib.util
import os
import sys
import types
from unittest import TestCase, mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class KeyMappingTests(TestCase):
    def _load_backend(self):
        spec = importlib.util.spec_from_file_location('kb_temp', os.path.join(ROOT, 'keyboard_backend.py'))
        module = importlib.util.module_from_spec(spec)
        dummy_pg = types.SimpleNamespace(
            FAILSAFE=False,
            press=mock.Mock(),
            hotkey=mock.Mock(),
            click=mock.Mock(),
        )
        with mock.patch.dict('sys.modules', {'pyautogui': dummy_pg}):
            spec.loader.exec_module(module)
        return module, dummy_pg

    def test_numpad_mapping(self):
        kb, dummy = self._load_backend()
        kb.send_key_combo('numpad_0')
        dummy.press.assert_called_once_with('num0')

    def test_mouse_click_mapping(self):
        kb, dummy = self._load_backend()
        kb.send_key_combo('left_click')
        dummy.click.assert_called_once_with(button='left')

    def test_function_key(self):
        kb, dummy = self._load_backend()
        kb.send_key_combo('f1')
        dummy.press.assert_called_once_with('f1')
