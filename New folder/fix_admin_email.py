import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

admin_func = """
            def send_admin_notification(user_email):
                try:
                    from .models import EmailConfiguration
                    email_config = EmailConfiguration.objects.first()
                    if email_config and email_config.subscription_email:
                        import re as regex
                        admin_emails = [e.strip() for e in regex.split(r'[,\s]+', email_config.subscription_email) if e.strip()]
                        if admin_emails:
                            admin_subject = "New Event Notification Subscriber!"
                            admin_message = f"Hello Admin,\\n\\nA new user has just subscribed to event notifications on the website:\\n\\nSubscriber Email: {user_email}\\n\\nBest regards,\\nSystem Notifications"
                            from django.core.mail import send_mail
                            send_mail(
                                admin_subject,
                                admin_message,
                                settings.DEFAULT_FROM_EMAIL,
                                admin_emails,
                                fail_silently=True,
                            )
                except Exception as e:
                    print(f"Error sending admin notification: {e}")
"""

# Insert admin_func after send_welcome_email
pattern = r"(except Exception as e:\s*print\(f\"Error sending welcome email: \{e\}\"\))"

if "def send_admin_notification" not in content:
    if re.search(pattern, content):
        content = re.sub(pattern, r"\1" + admin_func, content)
        
        # Also fix the if created: block to call it
        old_created = """            if created:
                send_welcome_email(email)
                messages.success"""
        new_created = """            if created:
                send_welcome_email(email)
                send_admin_notification(email)
                messages.success"""
        content = content.replace(old_created, new_created)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Admin notification function and logic successfully injected.")
    else:
        print("Failed to find send_welcome_email exception block.")
else:
    print("send_admin_notification already exists.")
