import os

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\dashboard\email_configuration_form.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "<div class=\"form-text\">Email address to receive Contact and Enquiry submissions.</div>",
    "<div class=\"form-text\">Email address to receive Contact and Enquiry submissions. <strong>(Separate multiple emails with commas)</strong></div>"
)
content = content.replace(
    "<div class=\"form-text\">Email address to receive Meeting Booking requests.</div>",
    "<div class=\"form-text\">Email address to receive Meeting Booking requests. <strong>(Separate multiple emails with commas)</strong></div>"
)
content = content.replace(
    "<div class=\"form-text\">Email address to receive Job Applications.</div>",
    "<div class=\"form-text\">Email address to receive Job Applications. <strong>(Separate multiple emails with commas)</strong></div>"
)
content = content.replace(
    "<div class=\"form-text\">Email address to receive Subscription notifications.</div>",
    "<div class=\"form-text\">Email address to receive Subscription notifications. <strong>(Separate multiple emails with commas)</strong></div>"
)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Template patched successfully')
