import unittest
from unittest.mock import patch, MagicMock
import sys, types, os
# Ensure repo root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock pyautogui to import app.app
mock_pg = types.SimpleNamespace(FAILSAFE=False, press=lambda *a, **k: None, hotkey=lambda *a, **k: None)
sys.modules['pyautogui'] = mock_pg

from app.app import run_shell_command

class ShellCommandTests(unittest.TestCase):
    def test_valid_command(self):
        mock_proc = MagicMock(stdout='ok', returncode=0)
        with patch('subprocess.run', return_value=mock_proc) as run:
            result = run_shell_command('echo test')
            run.assert_called_once()
            self.assertEqual(result, mock_proc)

    def test_invalid_command_chars(self):
        with self.assertRaises(ValueError):
            run_shell_command('rm -rf /; echo hi')

if __name__ == '__main__':
    unittest.main()
