# Delete application
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobApplication, UserSettings, UserProfile, Response, Resume, ApplicationCategory, AppearanceSettings, AccessibilitySettings
from .forms import SettingsForm, CustomUserCreationForm, CustomAuthenticationForm, NotificationSettingsForm, ApplicationCategoryForm, AppearanceSettingsForm, AccessibilitySettingsForm
import json
from .models import Resume
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
        # last 4 apps
        "recent_activity": user_applications.order_by("-created_at")[:4],
        "user": request.user,
    }
    return render(request, "home.html", context)

# Applications list with filtering


@login_required
def applications(request):
    applications_list = JobApplication.objects.filter(
        user=request.user).order_by('-date_applied')
    return render(request, "applications.html", {"applications": applications_list})


@login_required
def responses(request):
    # Get filter parameters
    response_type_filter = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '').strip()

    # Get user's responses
    responses_list = Response.objects.filter(
        user=request.user).order_by('-date')

    # Apply filters
    if response_type_filter != 'all':
        responses_list = responses_list.filter(
            response_type=response_type_filter)

    if search_query:
        responses_list = responses_list.filter(
            company__icontains=search_query
        ) | responses_list.filter(
            position__icontains=search_query
        )

    context = {
        'responses': responses_list,
        'active_filter': response_type_filter,
        'search_query': search_query
    }
    return render(request, "responses.html", context)


@login_required
def resumes(request):
    # Get user's resumes
    resumes_list = Resume.objects.filter(
        user=request.user).order_by('-updated_at')

    context = {
        "resumes": resumes_list,
        "page_title": "Resumes",
    }
    return render(request, "resumes.html", context)

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

    apps = JobApplication.objects.filter(
        user=request.user).order_by('-date_applied')

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


@login_required
def delete_application(request, app_id):
    from .models import JobApplication
    JobApplication.objects.filter(id=app_id, user=request.user).delete()
    return redirect('applications')


def get_resumes(request):
    resumes = Resume.objects.filter(user=request.user).order_by("-updated_at")
    data = [
        {
            "id": r.id,
            # or store a title field if you have one
            "title": r.title,
            "updated_at": r.updated_at.strftime("%b %d, %Y"),
        }
        for r in resumes
    ]
    return JsonResponse({"resumes": data})


def get_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return JsonResponse({
        "id": resume.id,
        "text": resume.text,
        "updated_at": resume.updated_at.strftime("%b %d, %Y")
    })


@login_required
def settings_view(request):
    # Get or create user-specific settings
    settings_obj, created = UserSettings.objects.get_or_create(
        user=request.user)

    # Get or create user profile
    profile, profile_created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = SettingsForm(request.POST, instance=settings_obj,
                            user=request.user, profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect("settings")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SettingsForm(instance=settings_obj,
                            user=request.user, profile=profile)

    context = {
        "form": form,
        "user": request.user,
        "profile": profile,
        "settings": settings_obj,
        "active_section": "profile"
    }
    return render(request, "settings.html", context)

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

# Response CRUD operations


@login_required
def add_response(request):
    if request.method == "POST":
        company = request.POST.get("company")
        position = request.POST.get("position")
        response_type = request.POST.get("response_type")
        date = request.POST.get("date")
        notes = request.POST.get("notes")
        next_action = request.POST.get("next_action")

        # Try to link to existing job application if company/position match
        job_app = None
        try:
            job_app = JobApplication.objects.filter(
                user=request.user,
                company__iexact=company,
                position__iexact=position
            ).first()
        except:
            pass

        Response.objects.create(
            user=request.user,
            job_application=job_app,
            company=company,
            position=position,
            response_type=response_type,
            date=date,
            notes=notes,
            next_action=next_action
        )
        messages.success(request, 'Response added successfully!')
        return redirect("responses")

    return render(request, "add_response.html")


@login_required
def edit_response(request, response_id):
    response_obj = get_object_or_404(
        Response, id=response_id, user=request.user)

    if request.method == "POST":
        response_obj.company = request.POST.get("company")
        response_obj.position = request.POST.get("position")
        response_obj.response_type = request.POST.get("response_type")
        response_obj.date = request.POST.get("date")
        response_obj.notes = request.POST.get("notes")
        response_obj.next_action = request.POST.get("next_action")
        response_obj.save()
        messages.success(request, 'Response updated successfully!')
        return redirect("responses")

    return render(request, "edit_response.html", {"response": response_obj})


@login_required
def delete_response(request, response_id):
    response_obj = get_object_or_404(
        Response, id=response_id, user=request.user)
    response_obj.delete()
    messages.success(request, 'Response deleted successfully!')
    return redirect("responses")


@csrf_exempt
@require_POST
def create_resume(request):
    data = json.loads(request.body)
    text = data.get("text", "")
    title = data.get("title", "Untitled Resume")

    resume = Resume.objects.create(
        user=request.user,
        text=text,
        title=title
    )

    return JsonResponse({
        "status": "ok",
        "resume_id": resume.id,
        "text": resume.text
    })


@csrf_exempt
@require_POST
def save_resume(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    resume_id = data.get("resume_id")
    if not resume_id:
        return JsonResponse({"error": "Missing resume_id"}, status=400)

    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
    except Resume.DoesNotExist:
        return JsonResponse({"error": "Resume not found"}, status=404)

    # Only update fields if provided
    text = data.get("text")
    title = data.get("title")

    updated = False
    if text is not None:
        resume.text = text
        updated = True
    if title is not None:
        resume.title = title
        updated = True

    if updated:
        resume.save()

    return JsonResponse({"status": "ok"})


@csrf_exempt
def delete_resume(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        resume_id = data.get("resume_id")

        if not resume_id:
            return JsonResponse({"error": "No resume ID provided"}, status=400)

        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            resume.delete()
            return JsonResponse({"success": True})
        except Resume.DoesNotExist:
            return JsonResponse({"error": "Resume not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)

# Resume CRUD operations


@login_required
def add_resume(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        summary = request.POST.get("summary")
        experience = request.POST.get("experience")
        education = request.POST.get("education")
        skills = request.POST.get("skills")
        is_master = request.POST.get("is_master") == "on"

        # If this is set as master, unset other masters
        if is_master:
            Resume.objects.filter(
                user=request.user, is_master=True).update(is_master=False)

        Resume.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            experience=experience,
            education=education,
            skills=skills,
            is_master=is_master
        )
        messages.success(request, 'Resume created successfully!')
        return redirect("resumes")

    return render(request, "add_resume.html")

# Settings Views


@login_required
def settings_notifications(request):
    settings_obj, created = UserSettings.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = NotificationSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Notification settings updated successfully!')
            return redirect("settings_notifications")
    else:
        form = NotificationSettingsForm(instance=settings_obj)

    context = {
        "form": form,
        "user": request.user,
        "settings": settings_obj,
        "active_section": "notifications"
    }
    return render(request, "settings.html", context)


@login_required
def settings_categories(request):
    categories = ApplicationCategory.objects.filter(
        user=request.user).order_by('name')

    if request.method == "POST":
        form = ApplicationCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect("settings_categories")
    else:
        form = ApplicationCategoryForm()

    context = {
        "form": form,
        "categories": categories,
        "user": request.user,
        "active_section": "categories"
    }
    return render(request, "settings.html", context)


@login_required
def settings_appearance(request):
    appearance_obj, created = AppearanceSettings.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = AppearanceSettingsForm(request.POST, instance=appearance_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Appearance settings updated successfully!')
            return redirect("settings_appearance")
    else:
        form = AppearanceSettingsForm(instance=appearance_obj)

    context = {
        "form": form,
        "user": request.user,
        "appearance": appearance_obj,
        "active_section": "appearance"
    }
    return render(request, "settings.html", context)


@login_required
def settings_accessibility(request):
    accessibility_obj, created = AccessibilitySettings.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = AccessibilitySettingsForm(
            request.POST, instance=accessibility_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Accessibility settings updated successfully!')
            return redirect("settings_accessibility")
    else:
        form = AccessibilitySettingsForm(instance=accessibility_obj)

    context = {
        "form": form,
        "user": request.user,
        "accessibility": accessibility_obj,
        "active_section": "accessibility"
    }
    return render(request, "settings.html", context)


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(
        ApplicationCategory, id=category_id, user=request.user)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect("settings_categories")
