from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("applications/", views.applications, name="applications"),
    path("settings/", views.settings, name="settings"),
    path("resumes/", views.resumes, name="resumes"),
    path("applications/add/", views.add_application, name="add_application")
    path("responses/", views.responses, name="responses"),
    path("applications/add/", views.add_application, name="add_application"),
    path("resumes/<int:resume_id>/download/", views.download_resume_pdf, name="download_resume_pdf"),
]

