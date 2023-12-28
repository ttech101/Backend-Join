from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Contact, Task

class YourAppTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_view(self):
        # Check if the login endpoint is functioning
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more checks based on your requirements
        self.assertIn('token', response.data)  # Check if the token is present in the response data

    def test_contact_creation(self):
        # Check if you can create a contact
        data = {'author': 'testuser', 'receiver': 'testuser', 'name': 'Test Contact', 'email': 'test@example.com', 'hex_color': '#FFFFFF', 'logogram': 'ABC'}
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add more checks based on your requirements
        contact = Contact.objects.get(name='Test Contact')
        self.assertEqual(contact.author.username, 'testuser')  # Check the author's username

    def test_task_creation(self):
        # Check if you can create a task
        data = {'headline': 'Test Task', 'text': 'Test task description', 'priority': 'High'}
        response = self.client.post(reverse('task'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add more checks based on your requirements
        task = Task.objects.get(headline='Test Task')
        self.assertEqual(task.text, 'Test task description')  # Example of an additional check

    # Add more tests for other functions

    def tearDown(self):
        # Clean up by deleting created objects or taking other necessary steps
        Contact.objects.all().delete()  # Example: Delete all created contacts
        Task.objects.all().delete()  # Example: Delete all created tasks