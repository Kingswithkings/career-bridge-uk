import unittest
from unittest.mock import patch

from fastapi import BackgroundTasks, HTTPException

from backend.app.api.routes import auth_routes
from backend.app.schemas.auth_schema import RegisterRequest
from backend.app.services import email_service


class WelcomeEmailTestCase(unittest.TestCase):
    def test_greeting_and_recipient(self):
        for name, greeting in [
            ("  Sarah   Jones ", "Hi Sarah,"),
            ("Anne-Marie Smith", "Hi Anne-Marie,"),
            ("Ada", "Hi Ada,"),
            (None, "Hi there,"),
            ("   ", "Hi there,"),
        ]:
            with self.subTest(name=name), patch.object(
                email_service, "_smtp_is_configured", return_value=True
            ), patch.object(email_service.smtplib, "SMTP") as smtp:
                self.assertTrue(email_service.send_registration_confirmation_email(
                    "new@example.com", name
                ))
                message = smtp.return_value.__enter__.return_value.send_message.call_args.args[0]
                self.assertEqual(message["To"], "new@example.com")
                self.assertEqual(message["Subject"], "Welcome to CareerBridge UK")
                self.assertTrue(message.get_content().startswith(greeting))

    def test_delivery_failure_returns_false(self):
        with patch.object(email_service, "_smtp_is_configured", return_value=True), patch.object(
            email_service.smtplib, "SMTP", side_effect=OSError("Unavailable")
        ), self.assertLogs(email_service.logger, level="ERROR"):
            self.assertFalse(email_service.send_registration_confirmation_email("new@example.com", "Ada"))

    def test_missing_configuration_skips_delivery(self):
        with patch.object(email_service, "_smtp_is_configured", return_value=False), patch.object(
            email_service.smtplib, "SMTP"
        ) as smtp:
            self.assertFalse(email_service.send_registration_confirmation_email("new@example.com"))
            smtp.assert_not_called()

    def test_successful_registration_queues_welcome(self):
        tasks = BackgroundTasks()
        request = RegisterRequest(email="new@example.com", password="secret", full_name="Sarah Jones")
        with patch.object(auth_routes, "register_user", return_value={"email": "new@example.com"}), patch.object(
            auth_routes, "posthog_client"
        ):
            auth_routes.register(request, tasks, db=None)
        self.assertEqual(len(tasks.tasks), 1)
        self.assertIs(tasks.tasks[0].func, email_service.send_registration_confirmation_email)
        self.assertEqual(tasks.tasks[0].args, ("new@example.com", "Sarah Jones"))

    def test_failed_registration_does_not_queue_welcome(self):
        tasks = BackgroundTasks()
        request = RegisterRequest(email="new@example.com", password="secret")
        with patch.object(auth_routes, "register_user", side_effect=HTTPException(400, "Email already registered")):
            with self.assertRaises(HTTPException):
                auth_routes.register(request, tasks, db=None)
        self.assertEqual(tasks.tasks, [])
