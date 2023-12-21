

from datetime import date
from django.conf import settings
from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateField(default=date.today)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')



class Task(models.Model):
    headline = models.CharField(max_length=150)
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    date = models.CharField(max_length=20)
    priority = models.CharField(max_length=30)
    category = models.JSONField()
    subtasks = models.JSONField()
    task_user = models.JSONField()
    task_board = models.CharField(max_length=40)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_tasks')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_tasks')