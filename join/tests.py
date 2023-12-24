from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Contact, Task

class YourAppTestCase(TestCase):
    def setUp(self):
        # Erstellen Sie einen Testbenutzer
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        # Erstellen Sie einen Token für den Testbenutzer
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_view(self):
        # Überprüfen Sie, ob der Anmeldungs-Endpunkt funktioniert
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Fügen Sie weitere Überprüfungen hinzu, basierend auf Ihren Anforderungen
        self.assertIn('token', response.data)  # Überprüfen Sie, ob der Token im Antwortdaten vorhanden ist

    def test_contact_creation(self):
        # Überprüfen Sie, ob Sie einen Kontakt erstellen können
        data = {'author': 'testuser', 'receiver': 'testuser', 'name': 'Test Contact', 'email': 'test@example.com', 'hex_color': '#FFFFFF', 'logogram': 'ABC'}
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Fügen Sie weitere Überprüfungen hinzu, basierend auf Ihren Anforderungen
        contact = Contact.objects.get(name='Test Contact')
        self.assertEqual(contact.author.username, 'testuser')  # Überprüfen Sie den Benutzernamen des Autors

    def test_task_creation(self):
        # Überprüfen Sie, ob Sie eine Aufgabe erstellen können
        data = {'headline': 'Test Task', 'text': 'Test task description', 'priority': 'High'}
        response = self.client.post(reverse('task'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Fügen Sie weitere Überprüfungen hinzu, basierend auf Ihren Anforderungen
        task = Task.objects.get(headline='Test Task')
        self.assertEqual(task.text, 'Test task description')  # Beispiel für eine zusätzliche Überprüfung

    # Fügen Sie weitere Tests für andere Funktionen hinzu

    def tearDown(self):
        # Räumen Sie auf, indem Sie erstellte Objekte löschen oder andere notwendige Schritte unternehmen
        Contact.objects.all().delete()  # Beispiel: Löschen Sie alle erstellten Kontakte
        Task.objects.all().delete()  # Beispiel: Löschen Sie alle erstellten Aufgaben