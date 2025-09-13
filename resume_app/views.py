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


def applications(request):
    applications_list = [
        {"company": "Tech Solutions Inc.", "position": "Frontend Developer", "date": "Jul 20, 2024", "status": "Interview"},
        {"company": "Global Innovations", "position": "UX/UI Designer", "date": "Jul 18, 2024", "status": "Applied"},
        {"company": "Creative Minds Studio", "position": "Product Manager", "date": "Jul 15, 2024", "status": "Offer"},
        {"company": "DataCorp Analytics", "position": "Data Scientist", "date": "Jul 10, 2024", "status": "Rejected"},
        {"company": "FutureTech Ventures", "position": "Software Engineer", "date": "Jul 05, 2024", "status": "Applied"},
        {"company": "Quantum Systems", "position": "DevOps Engineer", "date": "Jul 22, 2024", "status": "Interview"},
        {"company": "Cloud Solutions Ltd.", "position": "Cloud Architect", "date": "Jul 12, 2024", "status": "Applied"},
    ]
    return render(request, "applications.html", {"applications": applications_list})


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
