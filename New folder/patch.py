import os
import re

models_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\models.py"
forms_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\forms.py"
views_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

# --- Models ---
with open(models_path, 'r', encoding='utf-8') as f:
    m_content = f.read()

m_content = m_content.replace(
    "enquiry_email = models.EmailField(default='design1@biomedingredients.com', help_text=\"Email for Contact/Enquiries\")",
    "enquiry_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text=\"Email for Contact/Enquiries (comma separated for multiple)\")"
)
m_content = m_content.replace(
    "booking_email = models.EmailField(default='design1@biomedingredients.com', help_text=\"Email for Meeting Bookings\")",
    "booking_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text=\"Email for Meeting Bookings (comma separated for multiple)\")"
)
m_content = m_content.replace(
    "career_email = models.EmailField(default='design1@biomedingredients.com', help_text=\"Email for Career Applications\")",
    "career_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text=\"Email for Career Applications (comma separated for multiple)\")"
)
m_content = m_content.replace(
    "subscription_email = models.EmailField(default='design1@biomedingredients.com', help_text=\"Email for Subscriptions\")",
    "subscription_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text=\"Email for Subscriptions (comma separated for multiple)\")"
)

with open(models_path, 'w', encoding='utf-8') as f:
    f.write(m_content)

# --- Forms ---
with open(forms_path, 'r', encoding='utf-8') as f:
    f_content = f.read()

f_content = f_content.replace(
    "'enquiry_email': forms.EmailInput(attrs={'class': 'form-control'}),",
    "'enquiry_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email1@example.com, email2@example.com'}),"
)
f_content = f_content.replace(
    "'booking_email': forms.EmailInput(attrs={'class': 'form-control'}),",
    "'booking_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email1@example.com, email2@example.com'}),"
)
f_content = f_content.replace(
    "'career_email': forms.EmailInput(attrs={'class': 'form-control'}),",
    "'career_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email1@example.com, email2@example.com'}),"
)
f_content = f_content.replace(
    "'subscription_email': forms.EmailInput(attrs={'class': 'form-control'}),",
    "'subscription_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email1@example.com, email2@example.com'}),"
)

with open(forms_path, 'w', encoding='utf-8') as f:
    f.write(f_content)

# --- Views ---
with open(views_path, 'r', encoding='utf-8') as f:
    v_content = f.read()

# Pattern for enquiry_email
v_content = re.sub(
    r"recipient_email = email_config\.enquiry_email if email_config and email_config\.enquiry_email else 'design1@biomedingredients\.com'\n\s+send_mail\(\n\s+design_subject,\n\s+design_message,\n\s+settings\.DEFAULT_FROM_EMAIL,\n\s+\[recipient_email\],",
    r"email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'\n                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]\n                send_mail(\n                    design_subject,\n                    design_message,\n                    settings.DEFAULT_FROM_EMAIL,\n                    recipient_emails,",
    v_content
)

# Pattern for career_email
v_content = re.sub(
    r"recipient_email = email_config\.career_email if email_config and email_config\.career_email else 'design1@biomedingredients\.com'\n\s+send_mail\(\n\s+design_subject,\n\s+design_message,\n\s+settings\.DEFAULT_FROM_EMAIL,\n\s+\[recipient_email\],",
    r"email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'\n                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]\n                send_mail(\n                    design_subject,\n                    design_message,\n                    settings.DEFAULT_FROM_EMAIL,\n                    recipient_emails,",
    v_content
)

# Pattern for booking_email
v_content = re.sub(
    r"recipient_email = email_config\.booking_email if email_config and email_config\.booking_email else 'design1@biomedingredients\.com'\n\s+send_mail\(admin_subject, admin_message, settings\.DEFAULT_FROM_EMAIL, \[recipient_email\], fail_silently=True\)",
    r"email_str = email_config.booking_email if email_config and email_config.booking_email else 'design1@biomedingredients.com'\n              recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]\n              send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=True)",
    v_content
)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(v_content)

print('Patch applied successfully')
