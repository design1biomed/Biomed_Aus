import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmi_aus.settings')
django.setup()

from main.models import JobApplication

apps = JobApplication.objects.all().order_by('-id')[:5]
print("Recent applications:")
for app in apps:
    print(app.id, app.full_name, app.email, app.created_at)
