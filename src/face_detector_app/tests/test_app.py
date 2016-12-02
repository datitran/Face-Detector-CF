import os
import json
import unittest
from face_detector_app.app import app


class FaceDetectorAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def send_files(self, file_name):
        return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "rb").read()

    def test_main_page(self):
        """Test that the status code 200 is returned for get."""
        results = self.app.get("/")
        self.assertEqual(results.status_code, 200)

    def test_prediction_status(self):
        """Test that the status code 200 is returned for post."""
        results = self.app.post("/prediction", data=self.send_files("abba.png"), content_type="image/png")
        self.assertEqual(results.status_code, 200)

    def test_prediction_with_rectangle(self):
        """Test if the list is non-empty if there are faces."""
        results = self.app.post("/prediction", data=self.send_files("abba.png"), content_type="image/png")
        results_json = json.loads(results.data)
        self.assertGreater(len(results_json.get("faces")), 0)

    def test_prediction_no_rectangle(self):
        """Test if the list is empty if there are faces."""
        results = self.app.post("/prediction", data=self.send_files("landscape.png"), content_type="image/png")
        results_json = json.loads(results.data)
        self.assertEqual(len(results_json.get("faces")), 0)
