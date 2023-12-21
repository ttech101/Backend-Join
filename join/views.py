from django.forms import EmailField
from django.http import HttpResponse
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
from .models import Contact ,Task
from .serializers import ContactSerializer ,TaskSerializer
from .forms import CustomUserCreationForm
from rest_framework.permissions import IsAuthenticated

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
            'email': user.email,
            'contact': contact_serializer.data,  # Füge das serialisierte Contact-Objekt dem Response hinzu
            'task': task_serializer.data
        })



# class LoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         print('LoginView?')
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


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
            # GET-Anfrage für ein bestimmtes Kontaktobjekt
            contact = Contact.objects.get(pk=contact_id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        else:
            # GET-Anfrage für alle Kontaktobjekte
            contacts = Contact.objects.all()
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        # POST-Datenverarbeitungscode
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # PUT-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        contact = Contact.objects.get(pk=contact_id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE-Datenverarbeitungscode für ein bestimmtes Kontaktobjekt
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












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
            subject = 'Activate your account'
            message = render_to_string('registration_confirmation_email.html', {
                'user': user,
                'confirmation_link': f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}",
            })
            user.email_user(subject, message)
            return HttpResponse("Your response und nachricht sollte gesendet sein")
            # return render(request, 'registration/registration_complete.html', {'user': user})
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return HttpResponse("Your responsesss")
    # return render(request, 'registration/register.html', {'form': form})


