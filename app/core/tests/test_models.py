"""
Test for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class TestModels(TestCase):
    """ Test models."""

    def test_create_user_with_email_successful(self):
        """Test create user with email successful."""
        email = "test@example.com"
        password = "testpass123@"
        user = get_user_model().objects.create_user(
            email = email,
            password =  password,
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_norlmalized(self):
        """Test if main is normalized """

        sample_emails = [
            ["test1@Example.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@EXample.com", "test4@example.com"],
        ]

        for email, expected in sample_emails :
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def testnew_user_without_raises_error(self):
        """Test raising error when email not provided."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', "sample123")

    def test_create_superuser(self):
        """Test creation of a superuser"""
        user = get_user_model().objects.create_superuser(
            'superusertest@example.com',
            'superpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
