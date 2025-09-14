from django.db import models
from django.contrib.auth.models import User
class Response(models.Model):
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    next_action = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.position} ({self.type})"
    
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
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Model for the new job application form
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications', null=True, blank=True)
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
class UserSettings(models.Model):
    """Single-row settings for this app (no multi-user)."""
    display_name = models.CharField(max_length=100, default="Name")
    default_followup_days = models.PositiveIntegerField(default=7)
    email_notifications = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"Settings({self.display_name})"

