import unittest
from envshield.sanitizer import detect_secrets, mask_secret, sanitize_dict


class TestSanitizer(unittest.TestCase):
    def test_mask_secret(self):
        self.assertEqual(mask_secret("1234567890"), "12...90")
        self.assertEqual(mask_secret("abc"), "***")

    def test_detect_secrets(self):
        pat = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        detected = detect_secrets(f"export GITHUB_TOKEN={pat}")
        self.assertIn(pat, detected)

    def test_sanitize_dict(self):
        payload = {
            "app_name": "billing-service",
            "api_key": "secret-value-12345",
            "metadata": {
                "user_password": "supersecretpassword",
                "normal_field": "visible",
            },
        }
        sanitized = sanitize_dict(payload)
        self.assertEqual(sanitized["app_name"], "billing-service")
        self.assertNotEqual(sanitized["api_key"], "secret-value-12345")
        self.assertIn("...", sanitized["api_key"])
        self.assertNotEqual(sanitized["metadata"]["user_password"], "supersecretpassword")
        self.assertEqual(sanitized["metadata"]["normal_field"], "visible")


if __name__ == "__main__":
    unittest.main()
