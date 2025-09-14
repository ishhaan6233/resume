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
    path("get_resume/<int:resume_id>/", views.get_resume, name="get_resume"),
    path("get_resumes/", views.get_resumes, name="get_resumes"),
    path("create_resume/", views.create_resume, name="create_resume"),
    path("save_resume/", views.save_resume, name="save_resume"),
    path("delete_resume/", views.delete_resume, name="delete_resume"),
    path("responses/", views.responses, name="responses"),
    path("applications/add/", views.add_application, name="add_application"),
    path("applications/delete/<int:app_id>/",
         views.delete_application, name="delete_application"),
    path("settings/", views.settings_view, name="settings"),
    path("settings/notifications/", views.settings_notifications,
         name="settings_notifications"),
    path("settings/categories/", views.settings_categories,
         name="settings_categories"),
    path("settings/appearance/", views.settings_appearance,
         name="settings_appearance"),
    path("settings/accessibility/", views.settings_accessibility,
         name="settings_accessibility"),
    path("settings/categories/delete/<int:category_id>/",
         views.delete_category, name="delete_category"),

    # Response CRUD
    path("responses/add/", views.add_response, name="add_response"),
    path("responses/edit/<int:response_id>/",
         views.edit_response, name="edit_response"),
    path("responses/delete/<int:response_id>/",
         views.delete_response, name="delete_response"),
]
