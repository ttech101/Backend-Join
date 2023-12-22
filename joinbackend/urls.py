from django.contrib import admin
from django.urls import path

from join.views import LoginView, contact_view, delete_current_user, register, activate, task_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', register),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('contact/', contact_view, name='contact'),
    path('contact/<int:contact_id>/', contact_view, name='contact_detail'),
    path('task/', task_view, name='task'),
    path('task/<int:task_id>/', task_view, name='task_detail'),
    path('delete_current_user/', delete_current_user, name='delete_current_user'),
]
