from django.contrib import admin
from .models import NewUser, Message

# Register your models here.

admin.site.register(NewUser)
admin.site.register(Message)
