from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("applications/", views.applications_view, name="applications"),
    path("resumes/", views.resumes, name="resumes"),
<<<<<<< HEAD
    path("applications/add/", views.add_application, name="add_application")
=======
    path("responses/", views.responses, name="responses"),
    path("applications/add/", views.add_application, name="add_application"),
    path("resumes/<int:resume_id>/download/", views.download_resume_pdf, name="download_resume_pdf"),
>>>>>>> 16cbdabdbe94f08da41e65a84a03d3eac51b9ef0
]
