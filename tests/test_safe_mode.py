import unittest
from unittest.mock import patch
import sys, types, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mock_pg = types.SimpleNamespace(FAILSAFE=False, press=lambda *a, **k: None, hotkey=lambda *a, **k: None)
sys.modules['pyautogui'] = mock_pg

from app.app import app

class SafeModeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.post('/safe_mode', json={'enabled': False})

    def tearDown(self):
        self.client.post('/safe_mode', json={'enabled': False})

    def test_press_blocked_when_enabled(self):
        resp = self.client.post('/safe_mode', json={'enabled': True})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()['enabled'])
        resp2 = self.client.post('/press/1', json={'type': 'keys'})
        self.assertEqual(resp2.status_code, 403)
        self.assertEqual(resp2.get_json()['status'], 'error')

if __name__ == '__main__':
    unittest.main()
