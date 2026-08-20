import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# First we need to define the function. We'll insert it before if created:
target_block = """                except Exception as e:
                    print(f"Error sending welcome email: {e}")

            if created:"""

admin_func = """                except Exception as e:
                    print(f"Error sending welcome email: {e}")

            def send_admin_notification(user_email):
                try:
                    from .models import EmailConfiguration
                    email_config = EmailConfiguration.objects.first()
                    if email_config and email_config.subscription_email:
                        admin_emails = [e.strip() for e in email_config.subscription_email.replace(' ', ',').split(',') if e.strip()]
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

            if created:"""

content = content.replace(target_block, admin_func)

# Next, we need to call it in if created:
created_target = """            if created:
                send_welcome_email(email)
                messages.success(request, "You have successfully subscribed"""

created_new = """            if created:
                send_welcome_email(email)
                send_admin_notification(email)
                messages.success(request, "You have successfully subscribed"""

content = content.replace(created_target, created_new)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fix completed!")
