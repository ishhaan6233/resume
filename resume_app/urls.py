from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("applications/", views.applications, name="applications"),
    path("settings/", views.settings, name="settings"),
]