from app import app
import unittest

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Update how the test client is created
        self.tester = app.test_client()

    def test_home(self):
        response = self.tester.get('/')
        self.assertEqual(response.status_code, 200)
