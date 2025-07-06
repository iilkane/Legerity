from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from customer.models import User

# Create your tests here.

class RegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register(self):
        data={
            'email':'test2002@example.com',
            'password':'test',
            'fullname':'test123'
        }
        response=self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(email='test2002@example.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('test'))
        self.assertEqual(user.fullname, 'test123')

    def test_invalid_email(self):
        data = {
            'fullname': 'test',
            'email': 'email',
            'password': 'test'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.login_url=reverse('login')
        self.user=User.objects.create_user(
            email='test@example.com',
            password='test123',
            fullname='test'
        )

    def test_login(self):
        data={
            'email':'test@example.com',
            'password':'test123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        self.assertEqual(response.data['user']['fullname'], 'test')

    def test_login_invalid(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrong'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)