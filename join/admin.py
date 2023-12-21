from django.contrib import admin
from .models import Contact,Task

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','author','receiver')
    search_fields = ('name',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('headline','date','author','receiver')

admin.site.register(Task, TaskAdmin)

admin.site.register(Contact, ContactAdmin)