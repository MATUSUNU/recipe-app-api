"""
Tests for models.
"""
from django.test import TestCase
# WHENEVER WE WANTED TO UPDATE THE CUSTOM USER MODEL "get_user_model" make it happen
from django.contrib.auth import get_user_model # THIS IS HELPFUL FUNCTION INORDER TO GET PREFERENCE TO THE DJANGO CUSTOM MODEL

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_email_successful(self):
        """Test creating a user with an email is successful."""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password)) # TO CHECK THE PASSWORD IS HASHED OR NOT

