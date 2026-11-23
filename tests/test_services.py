import unittest
from datetime import timedelta
from unittest.mock import patch, MagicMock

import requests

from ipapp.api_client import ApiClient
from ipapp.exceptions import ApiError, IPNotAvailableError
from ipapp.services import PublicIPService, GeoLocationService


def fake_response(status=200, payload=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload
    resp.elapsed = timedelta(seconds=0.25)
    return resp


class TestApiClient(unittest.TestCase):
    def test_build_url_uses_urlencode(self):
        client = ApiClient("https://example.com")
        url = client._build_url("/x", {"q": "Tunis, TN", "format": "json"})
        self.assertEqual(url, "https://example.com/x?q=Tunis%2C+TN&format=json")

    @patch("ipapp.api_client.requests.get")
    def test_error_message_from_api(self, mock_get):
        mock_get.return_value = fake_response(401, {"message": "Wrong credentials"})
        with self.assertRaises(ApiError) as ctx:
            ApiClient("https://example.com")._get_json()
        self.assertIn("Wrong credentials", str(ctx.exception))
        self.assertIn("401", str(ctx.exception))

    @patch("ipapp.api_client.requests.get")
    def test_last_url_and_elapsed(self, mock_get):
        mock_get.return_value = fake_response(200, {"ok": True})
        client = ApiClient("https://example.com")
        client._get_json("/a", {"k": "v"})
        self.assertEqual(client.last_url, "https://example.com/a?k=v")
        self.assertAlmostEqual(client.last_elapsed, 0.25)


class TestServices(unittest.TestCase):
    @patch("ipapp.api_client.requests.get")
    def test_get_ipv4(self, mock_get):
        mock_get.return_value = fake_response(200, {"ip": "8.8.8.8"})
        self.assertEqual(PublicIPService().get_ipv4(), "8.8.8.8")

    @patch("ipapp.api_client.requests.get")
    def test_http_error(self, mock_get):
        mock_get.return_value = fake_response(401, {})
        with self.assertRaises(ApiError):
            PublicIPService().get_ipv4()

    @patch("ipapp.api_client.requests.get")
    def test_no_ipv6(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("no route")
        with self.assertRaises(IPNotAvailableError):
            PublicIPService().get_ipv6()

    @patch("ipapp.api_client.requests.get")
    def test_geo_missing_keys(self, mock_get):
        mock_get.return_value = fake_response(200, {"city": "Tunis"})
        info = GeoLocationService().get_info("8.8.8.8")
        self.assertEqual(info.city, "Tunis")
        self.assertIsNone(info.country)


if __name__ == "__main__":
    unittest.main()
