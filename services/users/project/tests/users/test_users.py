import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({
                    "username": "dgood",
                    "email": "danielgoodman5425@gmail.com"
                }),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("danielgoodman5425@gmail.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "daneilgoodman5425@gmail.com.org"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps({
                    "username": "dgood",
                    "email": "danielgoodman5425@gmail.com"
                }),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps({
                    "username": "dgood",
                    "email": "danielgoodman5425@gmail.com"
                }),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                "Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user(username="dgood", email="danielgoodman5425@gmail.com")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("dgood", data["data"]["username"])
            self.assertIn("danielgoodman5425@gmail.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        user_1 = add_user(username="dgood", email="danielgoodman5425@gmail.com").to_json()
        user_2 = add_user(username="cking", email="cking@gmail.com").to_json()
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEquals(response.status_code, 200)
            self.assertEquals(len(data["data"]["users"]), 2)


if __name__ == "__main__":
    unittest.main()
