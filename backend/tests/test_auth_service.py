import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base
from backend.app.models.user_model import User
from backend.app.services.auth_service import login_user, register_user


class AuthServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        testing_session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        Base.metadata.create_all(bind=self.engine)
        self.db = testing_session_local()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_register_and_login_normalizes_email_and_password(self):
        register_response = register_user(
            self.db,
            email=" USER@Example.COM ",
            password=" secret-password ",
            full_name=" Test User ",
        )

        self.assertEqual(register_response["email"], "user@example.com")

        user = self.db.query(User).filter(User.email == "user@example.com").one()
        self.assertEqual(user.full_name, "Test User")

        login_response = login_user(
            self.db,
            email="user@example.com",
            password="secret-password",
        )

        self.assertEqual(login_response["email"], "user@example.com")
        self.assertTrue(login_response["access_token"])

    def test_register_rejects_blank_password(self):
        with self.assertRaises(HTTPException) as exc_info:
            register_user(
                self.db,
                email="user@example.com",
                password="   ",
            )

        self.assertEqual(exc_info.exception.status_code, 400)
        self.assertEqual(exc_info.exception.detail, "Password is required")


if __name__ == "__main__":
    unittest.main()
