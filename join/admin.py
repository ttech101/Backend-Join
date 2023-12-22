from django.contrib import admin
from .models import Contact, Task, PasswordResetToken

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'author', 'receiver')
    search_fields = ('name',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('headline', 'date', 'author', 'receiver')

class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_password_token')

admin.site.register(Task, TaskAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)