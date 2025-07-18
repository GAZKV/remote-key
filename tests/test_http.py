import unittest
from unittest.mock import patch, MagicMock
import sys, types, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mock_pg = types.SimpleNamespace(FAILSAFE=False, press=lambda *a, **k: None, hotkey=lambda *a, **k: None)
sys.modules['pyautogui'] = mock_pg

from app.app import app, buttons

class HttpActionTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_press_http(self):
        buttons['1']['type'] = 'http'
        buttons['1']['method'] = 'POST'
        buttons['1']['url'] = 'http://example.com'
        buttons['1']['body'] = {'key': 'v'}
        mock_resp = MagicMock(status_code=201)
        with patch('app.app.requests.request', return_value=mock_resp) as req:
            resp = self.client.post('/press/1', json={'type': 'http'})
            self.assertEqual(resp.status_code, 200)
            req.assert_called_once_with('POST', 'http://example.com', json={'key': 'v'})
            self.assertEqual(resp.get_json()['status_code'], 201)

if __name__ == '__main__':
    unittest.main()
