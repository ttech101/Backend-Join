from django.contrib import admin
from django.urls import path
from join.views import LoginView, change_password, contact_view, delete_current_user, register, activate, task_view, reset_password



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('contact/', contact_view, name='contact'),
    path('contact/<int:contact_id>/', contact_view, name='contact_detail'),
    path('task/', task_view, name='task'),
    path('task/<int:task_id>/', task_view, name='task_detail'),
    path('delete_current_user/', delete_current_user, name='delete_current_user'),
    path('reset_password/', reset_password, name='reset_password'),
    path('change_password/', change_password, name='change_password'),
]
