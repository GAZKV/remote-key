import importlib.util
import os
import sys
import types
import ctypes
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

    def _load_backend_win(self, send_mock):
        spec = importlib.util.spec_from_file_location('kb_temp', os.path.join(ROOT, 'keyboard_backend.py'))
        module = importlib.util.module_from_spec(spec)
        with mock.patch.object(sys, 'platform', 'win32'):
            user32 = types.SimpleNamespace(SendInput=send_mock)
            with mock.patch.object(ctypes, 'WinDLL', return_value=user32, create=True):
                spec.loader.exec_module(module)
        return module

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

    def test_windows_sendinput_called(self):
        send_mock = mock.Mock(return_value=1)
        kb = self._load_backend_win(send_mock)
        kb.send_key_combo('a')
        self.assertEqual(kb.BACKEND_NAME, 'sendinput')
        self.assertEqual(kb.PLATFORM, 'windows')
        self.assertEqual(send_mock.call_count, 2)

        args1 = send_mock.call_args_list[0][0]
        ptr1 = ctypes.cast(args1[1], ctypes.POINTER(kb.INPUT))
        self.assertEqual(args1[0], 1)
        self.assertEqual(ptr1.contents.ki.wVk, 0x41)
        self.assertEqual(ptr1.contents.ki.dwFlags, 0)

        args2 = send_mock.call_args_list[1][0]
        ptr2 = ctypes.cast(args2[1], ctypes.POINTER(kb.INPUT))
        self.assertEqual(ptr2.contents.ki.wVk, 0x41)
        self.assertEqual(ptr2.contents.ki.dwFlags, kb.KEYEVENTF_KEYUP)

    def test_windows_sendinput_error(self):
        send_mock = mock.Mock(return_value=0)
        kb = self._load_backend_win(send_mock)
        def make_exc(code):
            exc = OSError(code, "err")
            exc.winerror = code
            return exc

        with mock.patch('ctypes.get_last_error', return_value=5, create=True), \
             mock.patch('ctypes.WinError', side_effect=make_exc, create=True):
            with self.assertRaises(OSError) as ctx:
                kb.send_key_combo('a')
        self.assertEqual(ctx.exception.winerror, 5)
