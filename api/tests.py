from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthApiTests(APITestCase):
    def test_register_user(self):
        url = '/api/register/'
        data = {
            'username': 'testuser',
            'password': 'TestPass123',
            'email': 'testuser@example.com',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='testlogin', password='TestPass123', email='login@example.com')
        url = '/api/auth/'
        data = {
            'username': 'testlogin',
            'password': 'TestPass123',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class ProfileApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='TestPass123', email='profile@example.com')
        auth_response = self.client.post('/api/auth/', {'username': 'profileuser', 'password': 'TestPass123'}, format='json')
        self.token = auth_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_get_profile(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')

    def test_update_profile(self):
        response = self.client.put('/api/profile/', {'first_name': 'John', 'last_name': 'Doe'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
