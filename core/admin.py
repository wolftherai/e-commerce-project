from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class SuperUser(UserAdmin):
    ordering = ['id']
    
admin.site.register(User, SuperUser) #add user table
