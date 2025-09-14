from .models import AppearanceSettings

def appearance(request):
    """
    Put the current user's appearance settings into every template.
    """
    if not request.user.is_authenticated:
        return {}

    # Ensure there is a row for this user
    settings, _ = AppearanceSettings.objects.get_or_create(user=request.user)

    # We send the raw theme (light/dark/auto). 'auto' is resolved client-side.
    return {
        "appearance": {
            "theme": settings.theme,                       # 'light' | 'dark' | 'auto'
            "primary_color": settings.primary_color or "#0d6efd",
            "font_size": settings.font_size or "medium",   # 'small' | 'medium' | 'large'
            "compact_mode": settings.compact_mode,         # True/False
        }
    }
