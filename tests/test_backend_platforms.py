import importlib.util
import os
import sys
import types
from unittest import TestCase, mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class BackendPlatformTests(TestCase):
    def _load_backend(self, platform):
        spec = importlib.util.spec_from_file_location('kb_temp', os.path.join(ROOT, 'keyboard_backend.py'))
        module = importlib.util.module_from_spec(spec)
        dummy_pg = types.SimpleNamespace(FAILSAFE=False, press=mock.Mock(), hotkey=mock.Mock())
        with mock.patch.object(sys, 'platform', platform):
            with mock.patch.dict('sys.modules', {'pyautogui': dummy_pg}):
                spec.loader.exec_module(module)
        return module, dummy_pg

    def test_linux_uses_pyautogui(self):
        kb, dummy = self._load_backend('linux')
        kb.send_key_combo('a')
        dummy.press.assert_called_once_with('a')
        self.assertEqual(kb.BACKEND_NAME, 'pyautogui')
        self.assertEqual(kb.PLATFORM, 'linux')

    def test_darwin_uses_pyautogui(self):
        kb, dummy = self._load_backend('darwin')
        kb.send_key_combo('b')
        dummy.press.assert_called_once_with('b')
        self.assertEqual(kb.BACKEND_NAME, 'pyautogui')
        self.assertEqual(kb.PLATFORM, 'darwin')
