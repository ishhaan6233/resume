from django.shortcuts import render, redirect, get_object_or_404
from .models import Application

# Dashboard / Home
def home(request):
    context = {
        "applied_applications": Application.objects.filter(status="Applied").count(),
        "interviews_scheduled": Application.objects.filter(status="Interview").count(),
        "offers_received": Application.objects.filter(status="Offer").count(),
        "rejections": Application.objects.filter(status="Rejected").count(),
        "recent_activity": Application.objects.all().order_by("-date")[:4],  # last 4 apps
    }
    return render(request, "home.html", context)

# Applications list with filtering
def applications(request):
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
        date_applied = request.POST.get("date")
        status = request.POST.get("status")

        Application.objects.create(
            company=company,
            position=position,
            date=date_applied,
            status=status,
        )
        return redirect("applications")

    return render(request, "add_applications.html")


# Enhanced applications view with search and filter
def applications_view(request):
    active_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()

    apps = Application.objects.all()

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