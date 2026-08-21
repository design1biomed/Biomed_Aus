import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """            def send_welcome_email(user_email):
                subject = "Welcome to Bio Med Ingredients Event Notifications!"
                message = "Hello,\n\nThank you for subscribing to our event notifications! We will let you know whenever we post new exhibition events so you can stay up to date.\n\nBest regards,\nBio Med Ingredients"
                try:
                      send_mail(
                        subject,
                        message,
                          settings.DEFAULT_FROM_EMAIL,
                        [user_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Error sending welcome email: {e}")

            if created:
                send_welcome_email(email)"""

new_block = """            def send_welcome_email(user_email):
                subject = "Welcome to Bio Med Ingredients Event Notifications!"
                message = "Hello,\\n\\nThank you for subscribing to our event notifications! We will let you know whenever we post new exhibition events so you can stay up to date.\\n\\nBest regards,\\nBio Med Ingredients"
                try:
                      send_mail(
                        subject,
                        message,
                          settings.DEFAULT_FROM_EMAIL,
                        [user_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Error sending welcome email: {e}")
                    
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
                            send_mail(
                                admin_subject,
                                admin_message,
                                settings.DEFAULT_FROM_EMAIL,
                                admin_emails,
                                fail_silently=True,
                            )
                except Exception as e:
                    print(f"Error sending admin notification: {e}")

            if created:
                send_welcome_email(email)
                send_admin_notification(email)"""

if "def send_welcome_email" in content:
    import builtins
    content = content.replace(old_block, new_block)
    # also add it to the reactivation block
    reactivation_old = """                if not subscriber.is_active:
                    subscriber.is_active = True
                    subscriber.save()
                    send_welcome_email(email)
                    messages.success"""
                    
    reactivation_new = """                if not subscriber.is_active:
                    subscriber.is_active = True
                    subscriber.save()
                    send_welcome_email(email)
                    send_admin_notification(email)
                    messages.success"""
    content = content.replace(reactivation_old, reactivation_new)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Admin email notification logic successfully added!")
else:
    print("Target block not found.")
