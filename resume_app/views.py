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
