from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserSettings, UserProfile, ApplicationCategory, AppearanceSettings, AccessibilitySettings

class SettingsForm(forms.ModelForm):
    # User profile fields
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )
    
    class Meta:
        model = UserSettings
        fields = ["display_name", "default_followup_days", "email_notifications"]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "default_followup_days": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "email_notifications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        
        if profile:
            self.fields['phone'].initial = profile.phone
            self.fields['bio'].initial = profile.bio
    
    def save(self, commit=True):
        settings = super().save(commit=False)
        
        if commit:
            settings.save()
            
            # Update user information
            user = settings.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            
            # Update user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.bio = self.cleaned_data['bio']
            profile.save()
        
        return settings

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", 
            "placeholder": "Password"
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", 
            "placeholder": "Confirm Password"
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # No password restrictions - user can set any password they want
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['email_notifications']
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ApplicationCategoryForm(forms.ModelForm):
    class Meta:
        model = ApplicationCategory
        fields = ['name', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AppearanceSettingsForm(forms.ModelForm):
    class Meta:
        model = AppearanceSettings
        fields = ['theme', 'primary_color', 'font_size', 'compact_mode']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'font_size': forms.Select(attrs={'class': 'form-control'}),
            'compact_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AccessibilitySettingsForm(forms.ModelForm):
    class Meta:
        model = AccessibilitySettings
        fields = ['high_contrast', 'reduced_motion', 'screen_reader_friendly', 'keyboard_navigation', 'focus_indicators']
        widgets = {
            'high_contrast': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reduced_motion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'screen_reader_friendly': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'keyboard_navigation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'focus_indicators': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
