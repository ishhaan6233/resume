from django import forms
from .models import UserSettings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ["display_name", "default_followup_days", "email_notifications"]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "default_followup_days": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "email_notifications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
