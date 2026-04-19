import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class PredictionViewsTests(TestCase):
    def test_dashboard_page_renders(self):
        response = self.client.get(reverse("predictor:predict"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tropical Cyclone Dashboard")
        self.assertContains(response, "Shelter Locator")
        self.assertContains(response, "Disaster History")
        self.assertContains(response, "Damage Reporting")
        self.assertContains(response, "AI Chat Assistant")
        self.assertContains(response, "Switch to Admin Mode")

    @patch("predictor.views.load_model_assets")
    def test_prediction_api_returns_enhanced_response(self, mock_load_model_assets):
        class DummyScaler:
            def transform(self, values):
                return values

        class DummyEstimator:
            def __init__(self, value):
                self.value = value

            def predict(self, values):
                return [self.value]

        class DummyModel:
            estimators_ = [DummyEstimator(64.0), DummyEstimator(66.0), DummyEstimator(65.0)]

            def predict(self, values):
                return [65.0]

        mock_load_model_assets.return_value = (DummyModel(), DummyScaler())

        payload = {
            "international_number_id": 1,
            "tropical_cyclone_number": 2,
            "tropical_cyclone_end_record": 3,
            "number_of_hours": 6,
            "grade": 4,
            "latitude": 18.5,
            "longitude": 72.8,
            "minimum_central_pressure": 950,
        }

        response = self.client.post(
            reverse("predictor:predict_api"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(set(data.keys()), {"floodLevel", "prediction", "confidence"})
        self.assertEqual(data["prediction"], 65.0)
        self.assertGreaterEqual(data["confidence"], 55.0)

    def test_prediction_api_rejects_bad_payload(self):
        response = self.client.post(
            reverse("predictor:predict_api"),
            data=json.dumps({"grade": "bad"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_chat_api_returns_local_risk_response(self):
        response = self.client.post(
            reverse("predictor:chat_api"),
            data=json.dumps({"message": "What does high risk mean?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Risk summary:", response.json()["response"])
        self.assertIn("Move away from low-lying", response.json()["response"])

    def test_chat_api_explains_website_features(self):
        response = self.client.post(
            reverse("predictor:chat_api"),
            data=json.dumps({"message": "How do I use the map and alerts on this website?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Website help:", response.json()["response"])
        self.assertIn("Check the map", response.json()["response"])
