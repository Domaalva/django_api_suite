from django.test import TestCase
from rest_framework.test import APIClient


class DemoRestApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_returns_only_active_items(self):
        response = self.client.get("/demo/rest/api/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(item["is_active"] for item in response.json()))

    def test_post_creates_item(self):
        response = self.client.post(
            "/demo/rest/api/",
            {"name": "User04", "email": "user04@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["name"], "User04")
        self.assertTrue(response.json()["data"]["is_active"])
