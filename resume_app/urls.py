from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path("", views.landing, name="landing"),
    
    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    
    # Protected pages
    path("dashboard/", views.home, name="home"),
    path("applications/", views.applications_view, name="applications"),
    path("resumes/", views.resumes, name="resumes"),
    path("responses/", views.responses, name="responses"),
    path("applications/add/", views.add_application, name="add_application"),
    path("applications/delete/<int:app_id>/", views.delete_application, name="delete_application"),
    path("settings/", views.settings_view, name="settings"),
    path("communications/add/", views.add_communication, name="add_communication"),
    path("metrics/", views.metrics, name="metrics"),
]
