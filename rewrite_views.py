import ast

def replace_function(file_path, func_name, new_code):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            start = node.lineno - 1
            end = node.end_lineno
            lines = source.splitlines()
            new_lines = lines[:start] + new_code.strip().splitlines() + lines[end:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines) + '\n')
            return True
    return False

path = r'C:\Users\Biomed\Documents\biomed\biomed_app\views.py'

contact_code = '''
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone", "")
        country = request.POST.get("country", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        product_name = request.POST.get("product_name", "")

        if product_name and not subject:
            subject = f"Inquiry about {product_name}"

        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone, country=country, subject=subject, message=message,
            )
            
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                from biomed_app.models import EmailConfiguration
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                design_subject = f"New Contact Message: {subject}" if subject else "New Contact Message"
                context = {
                    'name': name,
                    'email': email,
                    'phone': phone or 'N/A',
                    'subject': subject or 'General Inquiry',
                    'message': message
                }
                html_content = render_to_string('biomed_app/emails/contact_admin.html', context)
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg.attach_alternative(html_content, 'text/html')
                msg.send(fail_silently=True)
            except Exception as e:
                print(f"Error sending contact notification: {e}")
                
            messages.success(request, "Your message has been sent successfully!")
            return redirect(request.META.get("HTTP_REFERER", "contact"))

    return render(request, "biomed_app/contact.html")
'''

enquire_code = '''
def enquire(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone", "")
        country = request.POST.get("country", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone, country=country, subject=f"Inquiry about {subject}" if subject else "General Inquiry", message=message,
            )
            
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                from biomed_app.models import EmailConfiguration
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                design_subject = f"New Enquiry: {subject}" if subject else "New General Enquiry"
                context = {
                    'name': name,
                    'email': email,
                    'phone': phone or 'N/A',
                    'company': request.POST.get('company', 'N/A'),
                    'country': country or 'N/A',
                    'product_name': subject or 'General Inquiry',
                    'message': message
                }
                html_content = render_to_string('biomed_app/emails/enquiry_admin.html', context)
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg.attach_alternative(html_content, 'text/html')
                msg.send(fail_silently=True)
            except Exception as e:
                print(f"Error sending enquiry notification to design team: {e}")
                
            messages.success(request, "Your inquiry has been sent successfully!")
            return redirect("enquire")

    return render(request, "biomed_app/enquire.html")
'''

subscribe_code = '''
def subscribe_event_notifications(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = EventSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Successfully subscribed to event notifications!")
                
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.conf import settings
                    from django.template.loader import render_to_string
                    from django.utils.html import strip_tags
                    from biomed_app.models import EmailConfiguration
                    
                    email_config = EmailConfiguration.objects.first()
                    email_str = email_config.subscription_email if email_config and email_config.subscription_email else 'design1@biomedingredients.com'
                    recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                    
                    design_subject = "New Event Notification Subscriber"
                    context = {
                        'email': email,
                        'date': subscriber.subscribed_at.strftime('%B %d, %Y %I:%M %p') if hasattr(subscriber, 'subscribed_at') else "Just now"
                    }
                    html_content = render_to_string('biomed_app/emails/subscription_admin.html', context)
                    text_content = strip_tags(html_content)
                    
                    msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send(fail_silently=True)
                except Exception as e:
                    print(f"Error sending subscription notification: {e}")
            else:
                messages.info(request, "You are already subscribed to event notifications.")
        else:
            messages.error(request, "Please provide a valid email address.")
    
    return redirect(request.META.get('HTTP_REFERER', 'news_events'))
'''

print(replace_function(path, 'contact', contact_code))
print(replace_function(path, 'enquire', enquire_code))
print(replace_function(path, 'subscribe_event_notifications', subscribe_code))
