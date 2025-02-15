from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, UserSettings


class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'strongpassword123',
            'full_name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')


class TokenObtainPairTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='strongpassword123'
        )

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='strongpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_profile_retrieve(self):
        url = reverse('profile-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')


class UserSettingsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='strongpassword123'
        )
        self.settings = UserSettings.objects.create(
            user=self.user, theme_mode='light')
        self.client.force_authenticate(user=self.user)

    def test_user_settings_retrieve(self):
        url = reverse('settings-detail', args=[self.settings.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['theme_mode'], 'light')
