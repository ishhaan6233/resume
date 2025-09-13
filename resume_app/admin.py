from django.contrib import admin

# Register your models here.
from .models import UserSettings
admin.site.register(UserSettings)