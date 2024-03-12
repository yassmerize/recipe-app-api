"""
Test User API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """ Create and return a new user for test"""
    return get_user_model().objects.create_user(params)

class PublicUsersTests(TestCase):
    """Test public features of a user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test user creation on sucess."""
        payload = {
            'email': 'test@example.com',
            'password': "pass123",
            'name': "test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload('password')))
        self.assertNotIn('password', res.data)

    def test_create_user_with_email_error(self):
        """Test error if  user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': "pass123",
            'name': "test name",
        }
        create_user(payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error whend password in less than 5 charts"""
        payload = {
            'email': 'test@example.com',
            'password': "pass123",
            'name': "test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )
        self.assertFalse(user_exists)
