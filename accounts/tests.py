from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client = Client()  # Django test client

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")  

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "Please enter a correct username and password")
