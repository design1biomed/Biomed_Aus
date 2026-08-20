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

apply_code = '''
def apply_now(request, job_id):
    job = get_object_or_404(JobOpening, pk=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                from biomed_app.models import EmailConfiguration
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                design_subject = f'New Job Application: {job.title}'
                html_content = render_to_string('biomed_app/emails/job_application.html', {'application': application})
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(design_subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg.attach_alternative(html_content, 'text/html')
                
                # Attach the resume if available
                if application.resume:
                    msg.attach(application.resume.name, application.resume.read())
                    
                msg.send(fail_silently=True)
            except Exception as e:
                print(f'Error sending job application notification to design team: {e}')
                
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('career_detail', pk=job.pk)
    else:
        form = JobApplicationForm()
    return render(request, 'biomed_app/apply_now.html', {'form': form, 'job': job})
'''

print(replace_function(path, 'apply_now', apply_code))
