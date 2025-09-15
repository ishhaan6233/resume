from django.db import models
from django.contrib.auth.models import User
    
class Application(models.Model):
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=20)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Resume(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='resumes', null=True, blank=True)
    title = models.CharField(max_length=255, default="Untitled Resume")
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username if self.user else 'No User'}"

# Model for the new job application form


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='job_applications', null=True, blank=True)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    date_applied = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ("Applied", "Applied"),
        ("Interview", "Interview"),
        ("Offer", "Offer"),
        ("Rejected", "Rejected"),
    ])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.position}"

class Response(models.Model):
    """Model for tracking communication responses from companies"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responses')
    job_application = models.ForeignKey(
        JobApplication, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    response_type = models.CharField(max_length=50, choices=[
        ("Interview", "Interview"),
        ("Offer", "Offer"),
        ("Rejection", "Rejection"),
        ("Follow-up", "Follow-up"),
        ("Other", "Other"),
    ])
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.response_type}"

class Response(models.Model):
    """Model for tracking communication responses from companies"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responses')
    job_application = models.ForeignKey(
        JobApplication, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    response_type = models.CharField(max_length=50, choices=[
        ("Interview", "Interview"),
        ("Offer", "Offer"),
        ("Rejection", "Rejection"),
        ("Follow-up", "Follow-up"),
        ("Other", "Other"),
    ])
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.response_type}"


class UserSettings(models.Model):
    """User-specific settings for the application."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='settings', null=True, blank=True)
    display_name = models.CharField(max_length=100, default="Name")
    default_followup_days = models.PositiveIntegerField(default=7)
    email_notifications = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"

    def __str__(self):
        return f"Settings for {self.user.username}"


class ApplicationCategory(models.Model):
    """Categories for organizing job applications"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='application_categories')
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7, default="#007bff", help_text="Hex color code")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Application Category"
        verbose_name_plural = "Application Categories"
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class AppearanceSettings(models.Model):
    """User appearance and theme settings"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='appearance_settings')
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ], default='light')
    primary_color = models.CharField(max_length=7, default="#007bff")
    font_size = models.CharField(max_length=10, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ], default='medium')
    compact_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"Appearance settings for {self.user.username}"


class AccessibilitySettings(models.Model):
    """User accessibility preferences"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='accessibility_settings')
    high_contrast = models.BooleanField(default=False)
    reduced_motion = models.BooleanField(default=False)
    screen_reader_friendly = models.BooleanField(default=False)
    keyboard_navigation = models.BooleanField(default=True)
    focus_indicators = models.BooleanField(default=True)

    def __str__(self):
        return f"Accessibility settings for {self.user.username}"
