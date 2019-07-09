from project.api.models import User
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """Tests For User Model"""

    def test_deserialization(self):
        """Test deserialization of User object"""
        user_json = User(username="dgood", email="danielgoodman5425@gmail.com").to_json()
        self.assertEqual(user_json["username"], "dgood")
        self.assertEqual(user_json["email"], "danielgoodman5425@gmail.com")
