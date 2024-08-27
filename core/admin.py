from django.contrib import admin
# from .models import User
from core import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass