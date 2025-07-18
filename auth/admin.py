from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Flag, User

admin.site.register(User, UserAdmin)
admin.site.register(Flag)