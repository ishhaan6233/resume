from django.shortcuts import render, redirect
from .models import UserSettings
from .forms import SettingsForm

def home(request):
    context = {
        "applied_applications": 56,
        "interviews_scheduled": 12,
        "offers_received": 3,
        "rejections": 8,
        "recent_activity": [
            {"text": "Interview scheduled with Tech Solutions for Senior Software Engineer.", "time": "2 hours ago"},
            {"text": "Application submitted for Product Manager role at InnovateCorp.", "time": "Yesterday"},
            {"text": "Job offer received from Global Dynamics for Data Scientist position.", "time": "3 days ago"},
            {"text": "Follow up with HR at Marketing Pro for Account Executive role.", "time": "4 days ago"},
        ]
    }
    return render(request, "home.html", context)


def applications(request):
    applications_list = [
        {"company": "Tech Solutions Inc.", "position": "Frontend Developer", "date": "Jul 20, 2024", "status": "Interview"},
        {"company": "Global Innovations", "position": "UX/UI Designer", "date": "Jul 18, 2024", "status": "Applied"},
        {"company": "Creative Minds Studio", "position": "Product Manager", "date": "Jul 15, 2024", "status": "Offer"},
        {"company": "DataCorp Analytics", "position": "Data Scientist", "date": "Jul 10, 2024", "status": "Rejected"},
        {"company": "FutureTech Ventures", "position": "Software Engineer", "date": "Jul 05, 2024", "status": "Applied"},
        {"company": "Quantum Systems", "position": "DevOps Engineer", "date": "Jul 22, 2024", "status": "Interview"},
        {"company": "Cloud Solutions Ltd.", "position": "Cloud Architect", "date": "Jul 12, 2024", "status": "Applied"},
    ]
    return render(request, "applications.html", {"applications": applications_list})


def settings_view(request):
    # ensure we always have one settings row
    settings_obj, _ = UserSettings.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = SettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            # simple success flash
            return redirect("settings")
    else:
        form = SettingsForm(instance=settings_obj)

    return render(request, "settings.html", {"form": form})