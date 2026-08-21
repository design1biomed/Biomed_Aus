import re

path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# enquiry block (occurs twice)
enquiry_bad = re.compile(
    r"(\s+)email_str = email_config\.enquiry_email if email_config and email_config\.enquiry_email else 'design1@biomedingredients\.com'\n.*?fail_silently=True,\n\s+\)", 
    re.DOTALL
)

def fix_enquiry(match):
    indent = match.group(1)
    inner_indent = indent + "    "
    return f"{indent}email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'\n{indent}recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]\n{indent}send_mail(\n{inner_indent}design_subject,\n{inner_indent}design_message,\n{inner_indent}settings.DEFAULT_FROM_EMAIL,\n{inner_indent}recipient_emails,\n{inner_indent}fail_silently=True,\n{indent})"

content = enquiry_bad.sub(fix_enquiry, content)

# career block
career_bad = re.compile(
    r"(\s+)email_str = email_config\.career_email if email_config and email_config\.career_email else 'design1@biomedingredients\.com'\n.*?fail_silently=True,\n\s+\)", 
    re.DOTALL
)

def fix_career(match):
    indent = match.group(1)
    inner_indent = indent + "    "
    return f"{indent}email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'\n{indent}recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]\n{indent}send_mail(\n{inner_indent}design_subject,\n{inner_indent}design_message,\n{inner_indent}settings.DEFAULT_FROM_EMAIL,\n{inner_indent}recipient_emails,\n{inner_indent}fail_silently=True,\n{indent})"

content = career_bad.sub(fix_career, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Views fixed via regex')
