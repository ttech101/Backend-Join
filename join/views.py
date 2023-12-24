from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes, permission_classes
from .functions import create_first_contact
from .models import Contact, PasswordResetToken ,Task
from .serializers import ContactSerializer ,TaskSerializer
from .forms import CustomUserCreationForm
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.crypto import get_random_string
User = get_user_model()
# Create your views here.

class LoginView(ObtainAuthToken):
    '''
    This class defines a custom login view in Django, extending the ObtainAuthToken view,
    where upon successful authentication, it generates or retrieves an authentication token
    for the user, fetches associated contacts and tasks for that user, and returns a response
    containing the user's token, ID, name, email, as well as serialized contact and task data.
    '''
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        contacts = Contact.objects.filter(author=user)
        tasks = Task.objects.filter(author=user)
        contact_serializer = ContactSerializer(contacts, many=True)
        task_serializer = TaskSerializer(tasks, many=True)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name' : user.first_name + ' ' + user.last_name,
            'email': user.email,
            'contact': contact_serializer.data,
            'task': task_serializer.data
        })


def activate(request, uidb64, token):
    '''
    This function is a Django view for user account activation.
    It decodes the provided user ID and token from base64, attempts to retrieve the corresponding user,
    and if the decoding is successful and the token is valid, it activates the user account by setting "is_active"
    to True, and renders a success page with a specified frontend URL; otherwise, it renders a failure page.
    '''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        url = settings.FRONTEND_URL
        return render(request, 'activation_complete.html', {'url': url})
    else:
        return render(request, 'activation_failed.html')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_view(request, contact_id=None):
    '''
    This function is a Django REST Framework view for handling CRUD operations
    (GET, POST, PUT, DELETE) on a contact resource. It is decorated with
    @api_view to specify the supported HTTP methods, @authentication_classes
    to use Token Authentication, and @permission_classes to require user authentication.
    '''
    if request.method == 'GET':
        '''
        If a contact_id is provided, it retrieves and returns the details of a specific contact.
        If no contact_id is provided, it retrieves and returns all contacts associated with the authenticated user.
        '''
        if contact_id:
            print(contact_id)
            contact = Contact.objects.get(pk=contact_id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        else:
            contacts = Contact.objects.filter(author=request.user)
            contact_serializer = ContactSerializer(contacts, many=True)
            return Response(contact_serializer.data)

    elif request.method == 'POST':
        '''
        Processes data from the request to create a new contact for the authenticated user.
        Returns the serialized contact data if successful, or validation errors if the data is invalid.
        '''
        author = request.user
        data = request.data.copy()
        data['author'] = author.id
        data['receiver'] = author.id
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        '''
        Processes data from the request to update an existing contact specified by contact_id for the authenticated user.
        Returns the updated serialized contact data if successful, or validation errors if the data is invalid.
        '''
        author = request.user
        task = Contact.objects.get(pk=contact_id)
        data = request.data.copy()
        data['author'] = author.id
        data['receiver'] = author.id
        serializer = ContactSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        '''
        Deletes the contact specified by contact_id for the authenticated user.
        Returns a response with a 204 status code (No Content) indicating a successful deletion.
        '''
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_view(request, task_id=None):
    '''
    This function is a Django REST Framework view for handling CRUD operations
    (GET, POST, PUT, DELETE) on a task resource. It is decorated with @api_view
    to specify the supported HTTP methods, @authentication_classes to use Token
    Authentication, and @permission_classes to require user authentication.
    '''
    if request.method == 'GET':
        '''
        If a task_id is provided, it retrieves and returns the details of a specific task.
        If no task_id is provided, it retrieves and returns all tasks associated with the authenticated user.
        '''
        if task_id:
            task = Task.objects.get(pk=task_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            tasks = Task.objects.filter(author=request.user)
            task_serializer = TaskSerializer(tasks, many=True)
            return Response(task_serializer.data)

    elif request.method == 'POST':
        '''
        Processes data from the request to create a new task for the authenticated user.
        Returns the serialized task data if successful, or validation errors if the data is invalid.
        '''
        author = request.user
        data = request.data.copy()
        data['author'] = author.id
        data['receiver'] = author.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        '''
        Processes data from the request to update an existing task specified by task_id for the authenticated user.
        Returns the updated serialized task data if successful, or validation errors if the data is invalid.
        '''
        author = request.user
        task = Task.objects.get(pk=task_id)
        data = request.data.copy()
        data['author'] = author.id
        data['receiver'] = author.id
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        '''
        Deletes the task specified by task_id for the authenticated user.
        Returns a response with a 204 status code (No Content) indicating a successful deletion.
        '''
        task = Task.objects.get(pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_current_user(request):
    '''
    This function is a Django REST Framework view designed to handle the deletion
    of the current user account. It is decorated with @api_view to specify that only
    POST requests are allowed, @authentication_classes to use Token Authentication,
    and @permission_classes to require user authentication.
    '''
    user = request.user
    try:
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def register(request):
    '''
    This function is a Django view for user registration. It is decorated with
    @csrf_exempt to exempt it from the CSRF token requirement. Here's a breakdown
    of the functionality:
    POST Method:
    Validates the incoming form data (presumably containing user registration information) using a custom form (CustomUserCreationForm).
    If the form is valid, it creates a new user with the provided information but sets the user's active status to False.
    Calls a function (create_first_contact) to create an initial entry in the contacts for the newly registered user.
    Generates a confirmation email containing an activation link.
    Attempts to send the confirmation email, and if successful, returns a JSON response indicating successful registration along with a message to check the email.
    If there is an error sending the email, it returns an HTTP response with an error message.
    GET Method:
    Renders the registration form (CustomUserCreationForm) for a GET request.
    '''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            create_first_contact(user)

            # Send confirmation email
            current_site = get_current_site(request)
            subject = 'Activate your account for Join'
            message = render_to_string('registration_confirmation_email.html', {
                'user': user,
                'confirmation_link': f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}",
            })

            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = 'html'

            try:
                email.send()
                return JsonResponse({'ok':"You have successfully registered. Please check your email!"})
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
        else:
            return JsonResponse({'error': 'Please check the email address'})

    else:
        form = CustomUserCreationForm()
    return HttpResponse("Your response")


class CustomPasswordResetView(PasswordResetView):
    '''
    This class is a custom implementation of the Django PasswordResetView class,
    extending its functionality. Specifically, it overrides the form_valid method,
    which is called when the form used for password reset is successfully validated.
    '''
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password reset email sent successfully!')
        return response

@api_view(['POST',])
@permission_classes([AllowAny])
def reset_password(request):
    '''
    This function is a Django REST Framework view for handling password reset requests.
    It is decorated with @api_view to specify that only POST requests are allowed
    and @permission_classes to allow any user, even those who are not authenticated (AllowAny).
    POST Method:
    Retrieves the email address from the request data.
    Checks if a user with the provided email address exists in the system.
    Generates a unique token for the password reset process.
    Creates or updates a PasswordResetToken model associated with the user and saves the generated token.
    Constructs a password reset link using the generated token and the frontend URL.
    Sends a password reset email containing the password reset link.
    Returns a JSON response indicating the success of sending the reset email.
    Non-POST Request:
    Returns a JSON response with an error message for any request that is not a POST request.
    '''
    if request.method == 'POST':
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'This email address does not exist in the system.'})
        token = get_random_string(length=32)
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        password_reset_token.reset_password_token = token
        password_reset_token.save()
        reset_link = f"{settings.FRONTEND_URL}/html/reset-pass.html?password-reset&token={token}"
        subject = 'Reset password'
        message = render_to_string('password_reset_email.html', {'user': user,'reset_link': reset_link})
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)
        return JsonResponse({'success': 'We have sent you an email to reset'})
    else:
        return JsonResponse({'error': 'invalid request'}, status=400)


@api_view(['POST',])
@permission_classes([AllowAny])
def change_password(request):
    '''
    This function is a Django REST Framework view for handling password change requests,
    presumably after a user has clicked on a password reset link sent via email.
    It is decorated with @api_view to specify that only POST requests are allowed,
    and @permission_classes to allow any user, even those who are not authenticated (AllowAny).
    POST Method:
    Retrieves the token and new password from the request data.
    Checks if the provided token is valid by querying the PasswordResetToken model.
    Retrieves the user associated with the token.
    Sets the new password for the user.
    Saves the user with the updated password.
    Deletes the token entry from the PasswordResetToken model.
    Returns a JSON response indicating the success of changing the password.
    Non-POST Request:
    Returns a JSON response with an error message for any request that is not a POST request.
    '''
    if request.method == 'POST':
        token = request.data.get('token')
        password = request.data.get('password')
        token_obj = get_object_or_404(PasswordResetToken, reset_password_token=token)
        user = token_obj.user
        user.set_password(password)
        user.save()
        token_obj.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)