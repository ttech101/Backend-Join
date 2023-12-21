from django.contrib import admin
from django.urls import path

from join.views import LoginView, register, activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', register),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
