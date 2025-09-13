from django.db import models

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

