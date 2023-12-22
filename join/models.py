from datetime import date
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateField(default=date.today)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    hex_color = models.CharField(max_length=10)
    logogram = models.CharField(max_length=5)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')



class Task(models.Model):
    headline = models.CharField(max_length=150,null=True)
    text = models.CharField(max_length=500,null=True)
    created_at = models.DateField(default=date.today,null=True)
    date = models.CharField(max_length=20,null=True)
    priority = models.CharField(max_length=30,null=True)
    category = models.JSONField(null=True)
    idBox = models.CharField(max_length=10,null=True)
    subtasks = models.JSONField(null=True)
    task_user = models.JSONField(null=True)
    task_board = models.CharField(max_length=40,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_tasks')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_tasks')

class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)