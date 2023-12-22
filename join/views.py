from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Contact, PasswordResetToken ,Task
from .serializers import ContactSerializer ,TaskSerializer
from .forms import CustomUserCreationForm
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


# Create your views here.


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Hier wird das Contact-Objekt für den eingeloggten Benutzer abgerufen
        contacts = Contact.objects.filter(author=user)
        tasks = Task.objects.filter(author=user)

        # Hier wird das Contact-Objekt serialisiert
        contact_serializer = ContactSerializer(contacts, many=True)
        task_serializer = TaskSerializer(tasks, many=True)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name' : user.first_name + ' ' + user.last_name,
            'email': user.email,
            'contact': contact_serializer.data,  # Füge das serialisierte Contact-Objekt dem Response hinzu
            'task': task_serializer.data
        })


User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Logge den Benutzer automatisch ein
        login(request, user)
        return render(request, 'activation_complete.html')
    else:
        return render(request, 'activation_failed.html')


def send_confirmation_email(user, confirmation_link):
    subject = 'Bestätige deine Registrierung'
    # Verwende render_to_string, um die HTML-E-Mail aus deinem Template zu generieren
    html_message = render_to_string('registration_confirmation_email.html', {'user': user, 'confirmation_link': confirmation_link})
    # Extrahiere den reinen Text aus der HTML-E-Mail (für E-Mail-Clients ohne HTML-Unterstützung)
    plain_message = strip_tags(html_message)
    # Sende die E-Mail
    send_mail(subject, plain_message, 'deine_email@example.com', [user.email], html_message=html_message)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_view(request, contact_id=None):
    if request.method == 'GET':
        if contact_id:
            print(contact_id)
            # GET-Anfrage für ein bestimmtes Kontaktobjekt
            contact = Contact.objects.get(pk=contact_id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        else:
            # GET-Anfrage für alle Kontaktobjekte
            contacts = Contact.objects.filter(author=request.user)
            contact_serializer = ContactSerializer(contacts, many=True)
            return Response(contact_serializer.data)


    elif request.method == 'POST':
        # POST-Datenverarbeitungscode
        author = request.user
        serializer = ContactSerializer(data={'author': author.id, 'receiver': author.id, 'email': request.data.get('email'), 'name': request.data.get('name'), 'hex_color': request.data.get('hex_color'), 'logogram': request.data.get('logogram'), 'phone_number': request.data.get('phone_number')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # PUT-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        author = request.user
        contact = Contact.objects.get(pk=contact_id)
        serializer = ContactSerializer(contact, data={'author': author.id, 'receiver': author.id, 'email': request.data.get('email'), 'name': request.data.get('name'), 'hex_color': request.data.get('hex_color'), 'logogram': request.data.get('logogram'), 'phone_number': request.data.get('phone_number')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_view(request, task_id=None):
    if request.method == 'GET':
        if task_id:
            print(task_id)
            # GET-Anfrage für ein bestimmtes Kontaktobjekt
            task = Task.objects.get(pk=task_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            # GET-Anfrage für alle Kontaktobjekte
            tasks = Task.objects.filter(author=request.user)
            task_serializer = TaskSerializer(tasks, many=True)
            return Response(task_serializer.data)


    elif request.method == 'POST':
        # POST-Datenverarbeitungscode
        author = request.user
        data = request.data.copy()  # Kopiere die Daten, um sie zu ändern
        # Füge 'author' und 'receiver' zu den Daten hinzu
        data['author'] = author.id
        data['receiver'] = author.id

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # PUT-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        author = request.user
        task = Task.objects.get(pk=task_id)
        data = request.data.copy()  # Kopiere die Daten, um sie zu ändern
        data['author'] = author.id
        data['receiver'] = author.id
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        task = Task.objects.get(pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_current_user(request):
    user = request.user
    try:
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send confirmation email
            current_site = get_current_site(request)
            subject = 'Activate your account for Join'
            message = render_to_string('registration_confirmation_email.html', {
                'user': user,
                'confirmation_link': f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}",
            })

            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

            try:
                email.send()
                return HttpResponse("Your response und Nachricht sollten gesendet sein")
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return HttpResponse("Your response")


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # Hier kannst du benutzerdefinierte Aktionen hinzufügen, z.B. eine Erfolgsmeldung anzeigen
        messages.success(self.request, 'Password reset email sent successfully!')
        return response


@api_view(['POST',])
@permission_classes([AllowAny])
def reset_password(request):
    if request.method == 'POST':
        email = request.data.get('email')

        # Überprüfe, ob die E-Mail-Adresse im System existiert
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Diese E-Mail-Adresse existiert nicht im System.'}, status=400)

        # Generiere einen eindeutigen Token für die Passwortrücksetzung
        token = get_random_string(length=32)

        # Erstelle oder aktualisiere den Token im PasswordResetToken-Modell
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        password_reset_token.reset_password_token = token
        password_reset_token.save()

        # Baue den Rücksetzungslink
        reset_link = f"{settings.FRONTEND_URL}/html/reset-pass.html?password-reset&token={token}"

        # Sende die Passwortrücksetzungs-E-Mail
        subject = 'Passwort zurücksetzen'
        message = f'Klicken Sie auf den Link, um Ihr Passwort zurückzusetzen: {reset_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)


@api_view(['POST',])
@permission_classes([AllowAny])
def change_password(request):
    if request.method == 'POST':
        token = request.data.get('token')
        password = request.data.get('password')

        # Überprüfe, ob der Token gültig ist
        token_obj = get_object_or_404(PasswordResetToken, reset_password_token=token)
        user = token_obj.user

        # Setze das neue Passwort für den Benutzer
        user.set_password(password)
        user.save()

        # Lösche den Token-Eintrag
        token_obj.delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)