from django.shortcuts import render, redirect, get_object_or_404
from .models import Application, JobApplication

# Dashboard / Home
def home(request):
    context = {
        "applied_applications": JobApplication.objects.filter(status="Applied").count(),
        "interviews_scheduled": JobApplication.objects.filter(status="Interview").count(),
        "offers_received": JobApplication.objects.filter(status="Offer").count(),
        "rejections": JobApplication.objects.filter(status="Rejected").count(),
        "recent_activity": JobApplication.objects.all().order_by("-created_at")[:4],  # last 4 apps
    }
    return render(request, "home.html", context)

# Applications list with filtering
def applications(request):
    applications_list = JobApplication.objects.all().order_by('-date_applied')
    return render(request, "applications.html", {"applications":applications_list})

def responses(request):
    responses_list = [
        {"company": "a", "position": "b", "type": "c", "date": "x", "notes": "b", "next_action": "idk"},
    ]
    return render(request, "responses.html", {"responses": responses_list})

def resumes(request):
    resumes_list = [
        {
            "id": 1,
            "name": "Master Resume",
            "created": "Jul 01, 2024",
            "updated": "Jul 20, 2024",
            "is_master": True,
        },
        {
            "id": 2,
            "name": "Software Engineer Resume",
            "created": "Jul 05, 2024",
            "updated": "Jul 18, 2024",
            "is_master": False,
        },
        {
            "id": 3,
            "name": "Data Scientist Resume",
            "created": "Jul 08, 2024",
            "updated": "Jul 15, 2024",
            "is_master": False,
        },
    ]

    context = {
        "resumes": resumes_list,
        "page_title": "Resumes",
    }
    return render(request, "resumes.html", context)
    status_filter = request.GET.get("status")  # e.g. ?status=Applied
    if status_filter and status_filter != "all":
        applications_list = Application.objects.filter(status=status_filter).order_by("-date")
    else:
        applications_list = Application.objects.all().order_by("-date")

    return render(request, "applications.html", {
        "applications": applications_list,
        "active_filter": status_filter or "all"
    })

# Add new application
def add_application(request):
    if request.method == "POST":
        company = request.POST.get("company")
        position = request.POST.get("position")
        url = request.POST.get("url")
        date_applied = request.POST.get("date_applied")
        status = request.POST.get("status")
        notes = request.POST.get("notes")

        JobApplication.objects.create(
            company=company,
            position=position,
            url=url,
            date_applied=date_applied,
            status=status,
            notes=notes
        )
        return redirect("applications")

    return render(request, "add_applications.html")


# Enhanced applications view with search and filter
def applications_view(request):
    active_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()

    apps = JobApplication.objects.all().order_by('-date_applied')

    if active_filter != 'all':
        apps = apps.filter(status=active_filter)

    if search_query:
        apps = apps.filter(
            company__icontains=search_query
        ) | apps.filter(
            position__icontains=search_query
        )

    context = {
        'applications': apps,
        'active_filter': active_filter,
        'search_query': search_query
    }
    return render(request, 'applications.html', context)