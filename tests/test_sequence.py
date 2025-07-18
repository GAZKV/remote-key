import unittest
from unittest.mock import patch
import sys, types, os
# Ensure repo root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Provide a dummy pyautogui so app.app can be imported without X server
mock_pg = types.SimpleNamespace(FAILSAFE=False, press=lambda *a, **k: None, hotkey=lambda *a, **k: None)
sys.modules['pyautogui'] = mock_pg

from app.app import send_key_sequence

class WaitParseTests(unittest.TestCase):
    def run_seq(self, seq):
        combos = []
        sleeps = []
        with patch('app.app.send_key_combo', side_effect=lambda c: combos.append(c)):
            with patch('time.sleep', side_effect=lambda t: sleeps.append(t)):
                send_key_sequence(seq)
        return combos, sleeps

    def test_wait_next_token(self):
        combos, sleeps = self.run_seq('a wait 1000 b')
        self.assertEqual(combos, ['a', 'b'])
        self.assertEqual(sleeps, [1.0])

    def test_wait_single_token(self):
        combos, sleeps = self.run_seq('a wait500ms b')
        self.assertEqual(combos, ['a', 'b'])
        self.assertEqual(sleeps, [0.5])

    def test_list_input(self):
        combos, sleeps = self.run_seq(['a', 'wait', '200', 'b'])
        self.assertEqual(combos, ['a', 'b'])
        self.assertEqual(sleeps, [0.2])

if __name__ == '__main__':
    unittest.main()
