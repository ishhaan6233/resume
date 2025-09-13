from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("applications/", views.applications_view, name="applications"),
    path("resumes/", views.resumes, name="resumes"),
    path("responses/", views.responses, name="responses"),
    path("applications/add/", views.add_application, name="add_application"),
    path("applications/delete/<int:app_id>/", views.delete_application, name="delete_application"),
    path("settings/", views.settings_view, name="settings"),
]
