import os

path = r'C:\Users\Biomed\Documents\biomed\biomed_app\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

contact_bad = '''            try:
                from django.core.mail import send_mail
                from django.conf import settings
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                send_mail(design_subject, design_message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=True)
            except Exception as e:
                print(f"Error sending enquiry notification: {e}")'''

contact_good = '''            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                context = {
                    "name": name,
                    "email": email,
                    "phone": phone or "N/A",
                    "subject": subject or "General Inquiry",
                    "message": message
                }
                html_content = render_to_string("biomed_app/emails/contact_admin.html", context)
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
            except Exception as e:
                print(f"Error sending contact notification: {e}")'''

if contact_bad in content:
    content = content.replace(contact_bad, contact_good)
    print("Replaced contact")
else:
    print("Could not find contact_bad block")

enquire_bad = '''            try:
                from django.core.mail import send_mail
                from django.conf import settings
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                send_mail(design_subject, design_message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=True)
            except Exception as e:
                print(f"Error sending enquiry notification to design team: {e}")'''

enquire_good = '''            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                context = {
                    "name": name,
                    "email": email,
                    "phone": phone or "N/A",
                    "company": request.POST.get('company', 'N/A'),
                    "country": country or "N/A",
                    "product_name": subject or "General Inquiry",
                    "message": message
                }
                html_content = render_to_string("biomed_app/emails/enquiry_admin.html", context)
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
            except Exception as e:
                print(f"Error sending enquiry notification to design team: {e}")'''

if enquire_bad in content:
    content = content.replace(enquire_bad, enquire_good)
    print("Replaced enquire")
else:
    print("Could not find enquire_bad block")
    
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
