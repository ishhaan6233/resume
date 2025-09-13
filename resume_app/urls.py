from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("applications/", views.applications_view, name="applications"),
    path("resumes/", views.resumes, name="resumes"),
    path("applications/add/", views.add_application, name="add_application")
]
