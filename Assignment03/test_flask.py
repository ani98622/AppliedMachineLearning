import unittest
import requests
import subprocess
import time

class TestFlaskAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the Flask server before running tests."""
        cls.server_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait until the server is up
        time.sleep(5)  # Increase if needed

    @classmethod
    def tearDownClass(cls):
        """Terminate the Flask server after tests."""
        cls.server_process.terminate()
        cls.server_process.wait()  # Ensure it fully terminates

    def test_flask_api(self):
        """Does the API return expected results?"""
        url = "http://127.0.0.1:5000/score"
        payload = {"text": "Call FREEPHONE 8005420578 now!, to win bike", "threshold": 0.7}

        response = requests.post(url, json=payload)
        
        # Ensure server is responding
        self.assertEqual(response.status_code, 200, "Flask server did not return a 200 status")

        data = response.json()

        # Validate response structure
        self.assertIn("prediction", data)
        self.assertIn("propensity", data)

        # Validate data types
        self.assertIsInstance(data["prediction"], int)
        self.assertIsInstance(data["propensity"], float)

        # Validate probability range
        self.assertGreaterEqual(data["propensity"], 0)
        self.assertLessEqual(data["propensity"], 1)

if __name__ == '__main__':
    unittest.main()
