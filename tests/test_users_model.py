import unittest
from app.models import User


class UserTestCase(unittest.TestCase):
    def test_password_setter(self):
        user1 = User(password='testpassword')
        self.assertTrue(user1.password_hash is not None)

    def test_no_password_getter(self):
        user1 = User(password='testpassword')
        with self.assertRaises(AttributeError):
            user1.password

    def test_password_verification(self):
        user1 = User(password='testthispass')
        self.assertTrue(user1.verify_password('testthispass'))
        self.assertFalse(user1.verify_password('somewrongpassword'))

    # this tests if the 2 users with same password are generating a different hash or not
    def test_salt_in_password(self):
        user1 = User(password='testthispass')
        user2 = User(password='testthispass')
        self.assertTrue(user1.password_hash != user2.password_hash)
