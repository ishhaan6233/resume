from resume_app.models import Application, JobApplication

def migrate_applications():
    for app in Application.objects.all():
        JobApplication.objects.create(
            company=app.company,
            position=app.position,
            url=None,  # No URL in old model
            date_applied=app.date,
            status=app.status,
            notes=None  # No notes in old model
        )
    print("Migration complete. All Application entries copied to JobApplication.")

if __name__ == "__main__":
    migrate_applications()
