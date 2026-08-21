import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore the contact view email logic:
broken_contact = r"(?s)# Send beautifully designed notification email with resume attachment.*?except Exception as e:\s*print\(f\"Error sending HTML application notification: \{e\}\"\)"

fixed_contact = """# Send notification email to design team
            design_subject = f"New Enquiry: {subject}" if subject else "New General Enquiry"
            design_message = (
                f"A new enquiry has been submitted.\\n\\n"
                f"Details:\\n"
                f"- Name: {name}\\n"
                f"- Email: {email}\\n"
                f"- Phone: {phone or 'N/A'}\\n"
                f"- Country: {country or 'N/A'}\\n"
                f"- Subject: {subject or 'General Inquiry'}\\n"
                f"- Message: {message}\\n"
            )
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'

                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]

                send_mail(
                    design_subject,
                    design_message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_emails,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending enquiry notification: {e}")"""

if re.search(broken_contact, content):
    content = re.sub(broken_contact, fixed_contact.replace('\\', '\\\\'), content, count=1)
    
    # Now we need to correctly apply the HTML email logic to apply_now view ONLY!
    # Let's find apply_now view's email block.
    apply_now_pattern = r"(?s)              # Send notification email to design team\n\s*design_subject = f\"New Job Application: \{job\.title\}\"\n\s*design_message = \(\n.*?\)\n\s*try:\n\s*from django\.core\.mail import send_mail\n\s*from django\.conf import settings.*?send_mail\(.*?\)\n\s*except Exception as e:\n\s*print\(f\"Error sending application notification: \{e\}\"\)"
    
    # If the print is different, let's just use a more robust regex for apply_now
    apply_now_robust = r"(?s)(application\.save\(\)\s*)# Send notification email to design team.*?except Exception as e:\s*print\(f\"Error sending .*?: \{e\}\"\)"
    
    new_apply_now = """\\1# Send beautifully designed notification email with resume attachment
              design_subject = f"New Job Application: {job.title} - {application.name}"
              
              try:
                  from django.core.mail import EmailMultiAlternatives
                  from django.conf import settings
                  from django.template.loader import render_to_string
                  from django.utils.html import strip_tags
                  import mimetypes

                  email_config = EmailConfiguration.objects.first()
                  email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'
                  recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]

                  # Render HTML template
                  html_content = render_to_string("biomed_app/emails/job_application.html", {
                      "application": application
                  })
                  # Create plaintext fallback
                  text_content = strip_tags(html_content)

                  msg = EmailMultiAlternatives(
                      design_subject,
                      text_content,
                      settings.DEFAULT_FROM_EMAIL,
                      recipient_emails
                  )
                  msg.attach_alternative(html_content, "text/html")
                  
                  # Attach Resume if it exists
                  if application.resume and application.resume.name:
                      content_type, _ = mimetypes.guess_type(application.resume.name)
                      content_type = content_type or 'application/octet-stream'
                      try:
                          msg.attach(application.resume.name.split('/')[-1], application.resume.read(), content_type)
                      except Exception as attach_e:
                          print(f"Could not attach resume: {attach_e}")

                  msg.send(fail_silently=True)
              except Exception as e:
                  print(f"Error sending HTML application notification: {e}")"""
    
    if re.search(apply_now_robust, content):
        content = re.sub(apply_now_robust, new_apply_now.replace('\\', '\\\\'), content, count=1)
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Restored contact view and successfully updated apply_now view!")
    else:
        print("Restored contact view but could not find apply_now block to replace.")
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
else:
    print("Could not find the broken contact block.")
