from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print('LoginView?')
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


@csrf_exempt
def register(request):
    if request.method == "POST":
        print('register?', request)
        username = request.POST.get('username')
        print('username:', username)  # Füge diese Zeile hinzu, um den Wert von 'username' zu überprüfen

        if username:
            User.objects.create_user(
                username = request.POST.get('username'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                password=request.POST.get('password1')
            )
            return HttpResponse("Your response")
        else:
            return HttpResponse("Username is required")


