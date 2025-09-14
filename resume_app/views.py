# Delete application
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Application, JobApplication, UserSettings, UserProfile
from .forms import SettingsForm, CustomUserCreationForm, CustomAuthenticationForm


# Landing page
def landing(request):
    return render(request, "landing.html")

# Dashboard / Home
@login_required
def home(request):
    # Get user's applications
    user_applications = JobApplication.objects.filter(user=request.user)
    
    context = {
        "applied_applications": user_applications.filter(status="Applied").count(),
        "interviews_scheduled": user_applications.filter(status="Interview").count(),
        "offers_received": user_applications.filter(status="Offer").count(),
        "rejections": user_applications.filter(status="Rejected").count(),
        "recent_activity": user_applications.order_by("-created_at")[:4],  # last 4 apps
        "user": request.user,
    }
    return render(request, "home.html", context)

# Applications list with filtering
@login_required
def applications(request):
    status_filter = request.GET.get("status")
    if status_filter and status_filter != "all":
        applications_list = JobApplication.objects.filter(status=status_filter).order_by("-date_applied")
    else:
        applications_list = JobApplication.objects.all().order_by("-date_applied")

    return render(request, "applications.html", {
        "applications": applications_list,
        "active_filter": status_filter or "all"
    })

@login_required
def responses(request):
    from .models import Response
    active_filter = request.GET.get('type', 'all')
    if active_filter == 'all':
        responses_list = Response.objects.all().order_by('-date')
    else:
        responses_list = Response.objects.filter(type=active_filter).order_by('-date')
    return render(request, "responses.html", {
        "responses": responses_list,
        "active_filter": active_filter
    })

@login_required
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
@login_required
def add_application(request):
    if request.method == "POST":
        company = request.POST.get("company")
        position = request.POST.get("position")
        url = request.POST.get("url")
        date_applied = request.POST.get("date_applied")
        status = request.POST.get("status")
        notes = request.POST.get("notes")

        JobApplication.objects.create(
            user=request.user,
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
@login_required
def applications_view(request):
    active_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()

    apps = JobApplication.objects.filter(user=request.user).order_by('-date_applied')

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

# Delete application
@login_required
def delete_application(request, app_id):
    from .models import JobApplication
    JobApplication.objects.filter(id=app_id, user=request.user).delete()
    return redirect('applications')

@login_required
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

# Authentication Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                
                # Log the user in
                login(request, user)
                
                # Set remember me cookie if requested
                if request.POST.get('remember_me'):
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # Session cookie
                
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Set remember me cookie if requested
                if request.POST.get('remember_me'):
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # Session cookie
                
                # Redirect to next page or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')
