import unittest

from ipapp.models import IPAddressInfo


class TestIPAddressInfo(unittest.TestCase):
    def test_ipv4(self):
        info = IPAddressInfo("8.8.8.8", country="US")
        self.assertEqual(info.version, 4)
        self.assertFalse(info.is_private)
        self.assertIn("US", str(info))

    def test_ipv6(self):
        info = IPAddressInfo("2001:4860:4860::8888")
        self.assertEqual(info.version, 6)

    def test_private(self):
        self.assertTrue(IPAddressInfo("192.168.1.10").is_private)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            IPAddressInfo("pas-une-ip")

    def test_to_dict(self):
        d = IPAddressInfo("1.1.1.1", city="Paris").to_dict()
        self.assertEqual(d["city"], "Paris")
        self.assertEqual(d["version"], 4)

    def test_address(self):
        info = IPAddressInfo("8.8.8.8")
        self.assertEqual(info.address, "8.8.8.8")

    def test_optional_information(self):
        info = IPAddressInfo("8.8.8.8", city="Tunis", country="TN")
        self.assertEqual(info.city, "Tunis")
        self.assertEqual(info.country, "TN")

    def test_string_representation(self):
        info = IPAddressInfo("8.8.8.8", city="Tunis")
        self.assertIn("8.8.8.8", str(info))
        self.assertIn("Tunis", str(info))
if __name__ == "__main__":
    unittest.main()
