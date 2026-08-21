import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmi_aus.settings')
django.setup()

from django.core.mail import send_mail

try:
    print("Attempting to send test email through Django...")
    send_mail(
        'Test Subject',
        'Test Message body.',
        'ajomonthomas741@gmail.com',
        ['ajomonthomas741@gmail.com'],
        fail_silently=False,
    )
    print("SUCCESS: Django sent the email successfully!")
except Exception as e:
    print("ERROR:")
    print(str(e))
