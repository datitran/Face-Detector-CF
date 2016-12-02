import os
import unittest
from face_detector_app.app import app

class FaceDetectorAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.files = {"files": open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "abba.png"), "rb")}

    def test_main_page(self):
        """Test that the status code 200 is returned for get."""
        results = self.app.get("/")
        self.assertEqual(results.status_code, 200)

    def test_prediction_status(self):
        """Test that the status code 200 is returned for post."""
        results = self.app.post("/prediction", data=self.files)
        self.assertEqual(results.status_code, 200)

    def test_sum_image(self):
        """To Add."""
        pass
