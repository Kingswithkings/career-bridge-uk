import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from backend.scripts.setup_zoho_mail import request_json


class ZohoSetupTestCase(unittest.TestCase):
    def test_http_errors_report_status_without_private_content(self):
        for body, expected in [
            (b'{"error":"invalid_code","secret":"PRIVATE"}', "invalid_code"),
            (b'{"error":"PRIVATE"}', "Zoho rejected"),
            (b'<html>PRIVATE</html>', "Zoho rejected"),
        ]:
            with self.subTest(body=body):
                error = HTTPError("https://accounts.zoho.com/oauth/v2/token", 400, "PRIVATE", {}, io.BytesIO(body))
                with patch("urllib.request.urlopen", side_effect=error):
                    with self.assertRaises(ValueError) as result:
                        request_json("https://accounts.zoho.com/oauth/v2/token", {"code": "PRIVATE"})
                message = str(result.exception)
                self.assertIn("Token exchange failed (HTTP 400)", message)
                self.assertIn(expected, message)
                self.assertNotIn("PRIVATE", message)

    def test_success_status_oauth_error_is_explained(self):
        with patch("urllib.request.urlopen") as opener:
            opener.return_value.__enter__.return_value = io.BytesIO(b'{"error":"invalid_client"}')
            with self.assertRaisesRegex(ValueError, "invalid_client"):
                request_json("https://accounts.zoho.com/oauth/v2/token")

    def test_account_lookup_rate_limit_identifies_stage(self):
        error = HTTPError("https://mail.zoho.com/api/accounts", 429, "", {}, io.BytesIO(b'{}'))
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaisesRegex(ValueError, "Account lookup failed.*429.*Too many attempts"):
                request_json("https://mail.zoho.com/api/accounts", token="PRIVATE")
