from django.shortcuts import render

def home(request):
    context = {
        "applied_applications": 56,
        "interviews_scheduled": 12,
        "offers_received": 3,
        "rejections": 8,
        "recent_activity": [
            {"text": "Interview scheduled with Tech Solutions for Senior Software Engineer.", "time": "2 hours ago"},
            {"text": "Application submitted for Product Manager role at InnovateCorp.", "time": "Yesterday"},
            {"text": "Job offer received from Global Dynamics for Data Scientist position.", "time": "3 days ago"},
            {"text": "Follow up with HR at Marketing Pro for Account Executive role.", "time": "4 days ago"},
        ]
    }
    return render(request, "home.html", context)
