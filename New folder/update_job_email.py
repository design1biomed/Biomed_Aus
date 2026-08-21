import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(?s)# Send notification email to design team.*?except Exception as e:\s*print\(f?\"Error sending.*?\"\)"

new_logic = """# Send beautifully designed notification email with resume attachment
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

if re.search(pattern, content):
    content = re.sub(pattern, new_logic.replace('\\', '\\\\'), content, count=1)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced email logic!")
else:
    print("Regex failed.")
