from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user_register')
        self.data = {
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'phone': '1234567890',
            'user_type': 'patient',
            'password': 'testpassword123',
        }

    def test_user_registration(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())
