import unittest
from unittest.mock import patch

import httpx

from backend.app.services import email_service, zoho_mail


class ZohoMailTestCase(unittest.TestCase):
    def setUp(self):
        settings = patch.multiple(zoho_mail.config, ZOHO_CLIENT_ID="client",
            ZOHO_CLIENT_SECRET="secret", ZOHO_REFRESH_TOKEN="refresh",
            ZOHO_ACCOUNT_ID="123", ZOHO_FROM_EMAIL="kings@1st-kings.com")
        settings.start()
        self.addCleanup(settings.stop)
        zoho_mail._access_token = None
        zoho_mail._expires_at = 0
        self.calls = []

    def transport(self, request):
        import json
        self.calls.append(request)
        if request.url.host == "accounts.zoho.com":
            self.assertNotIn("secret", str(request.url))
            return httpx.Response(200, json={"access_token": "access", "expires_in": 3600})
        self.assertEqual(request.headers["Authorization"], "Zoho-oauthtoken access")
        payload = json.loads(request.content)
        self.assertEqual(payload["fromAddress"], "kings@1st-kings.com")
        self.assertEqual(payload["toAddress"], "new@example.com")
        self.assertEqual(payload["mailFormat"], "plaintext")
        self.assertIn("Hi Sarah,", payload["content"])
        return httpx.Response(200, json={"status": {"code": 200}})

    def test_welcome_and_reset_use_https_and_reuse_token(self):
        client = httpx.Client(transport=httpx.MockTransport(self.transport))
        with patch.object(zoho_mail.httpx, "Client", return_value=client), patch.object(email_service.smtplib, "SMTP") as smtp:
            self.assertTrue(email_service.send_registration_confirmation_email("new@example.com", "Sarah Jones"))
            smtp.assert_not_called()
        client = httpx.Client(transport=httpx.MockTransport(self.transport))
        with patch.object(zoho_mail.httpx, "Client", return_value=client):
            self.assertTrue(email_service.send_password_reset_code("new@example.com", "123456", "Sarah"))
        self.assertEqual(len(self.calls), 3)

    def test_expired_token_is_refreshed(self):
        zoho_mail._access_token = "expired"
        client = httpx.Client(transport=httpx.MockTransport(self.transport))
        with patch.object(zoho_mail.httpx, "Client", return_value=client):
            self.assertTrue(email_service.send_registration_confirmation_email("new@example.com", "Sarah"))
        self.assertEqual(len(self.calls), 2)

    def test_provider_errors_fail_without_logging_secrets(self):
        for status, body in [(200, {"error": "secret"}), (401, {}), (429, {}), (200, {"status": {"code": 500}})]:
            with self.subTest(status=status, body=body):
                zoho_mail._access_token = "access"
                zoho_mail._expires_at = float("inf")
                client = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(status, json=body)))
                with patch.object(zoho_mail.httpx, "Client", return_value=client), self.assertLogs(zoho_mail.logger, level="ERROR") as logs:
                    self.assertFalse(email_service.send_registration_confirmation_email("new@example.com", "Sarah"))
                self.assertNotIn("secret", " ".join(logs.output))

    def test_incomplete_settings_do_not_fall_back_to_smtp(self):
        with patch.object(zoho_mail.config, "ZOHO_REFRESH_TOKEN", None), patch.object(email_service.smtplib, "SMTP") as smtp, self.assertLogs(zoho_mail.logger, level="ERROR"):
            self.assertFalse(email_service.send_registration_confirmation_email("new@example.com", "Sarah"))
            smtp.assert_not_called()
