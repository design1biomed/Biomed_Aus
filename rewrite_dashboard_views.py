import ast

def replace_function(file_path, func_name, new_code):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # We might have duplicates, so we find all and replace the first, delete the rest, or just replace all instances with nothing and then insert the new code where the last one was.
    # A simpler approach: regex or just manual AST.
    tree = ast.parse(source)
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == func_name]
    if not nodes:
        return False
        
    lines = source.splitlines()
    
    # Process from bottom to top to avoid shifting line numbers
    for i, node in enumerate(reversed(nodes)):
        start = node.lineno - 1
        end = node.end_lineno
        if i == 0: # This is the last one in the file (top of reversed list) - replace with new code
            lines = lines[:start] + new_code.strip().splitlines() + lines[end:]
        else: # Remove earlier duplicates
            lines = lines[:start] + lines[end:]
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    return True

path = r'C:\Users\Biomed\Documents\biomed\biomed_app\dashboard_views.py'

accept_code = '''
@login_required(login_url='dashboard_login')
def expo_meeting_booking_accept(request, pk):
    booking = get_object_or_404(ExpoMeetingBooking, pk=pk)
    if booking.status != 'accepted':
        booking.status = 'accepted'
        booking.save()
        subject = f'Meeting Accepted: {booking.expo.tag}'
        
        context = {
            'name': booking.name,
            'event_title': booking.expo.tag,
            'date': booking.meeting_date.strftime('%B %d, %Y') if booking.meeting_date else 'TBD',
            'time': booking.meeting_time.strftime('%I:%M %p') if booking.meeting_time else 'TBD',
            'status': 'accepted',
        }
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        html_content = render_to_string('biomed_app/emails/expo_booking_update.html', context)
        text_content = strip_tags(html_content)
        try:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [booking.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=False)
            messages.success(request, f'Meeting request from {booking.name} accepted and email sent.')
        except Exception as e:
            print(f'Error sending meeting acceptance email: {e}')
            messages.warning(request, f'Meeting request from {booking.name} accepted, but failed to send email.')
    else:
        messages.info(request, f'Meeting request from {booking.name} is already accepted.')
    return redirect('dashboard_expo_meeting_bookings')
'''

reject_code = '''
@login_required(login_url='dashboard_login')
def expo_meeting_booking_reject(request, pk):
    booking = get_object_or_404(ExpoMeetingBooking, pk=pk)
    if booking.status != 'rejected':
        booking.status = 'rejected'
        booking.save()
        subject = f'Meeting Request Update: {booking.expo.tag}'
        
        context = {
            'name': booking.name,
            'event_title': booking.expo.tag,
            'date': booking.meeting_date.strftime('%B %d, %Y') if booking.meeting_date else 'TBD',
            'time': booking.meeting_time.strftime('%I:%M %p') if booking.meeting_time else 'TBD',
            'status': 'rejected',
        }
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        html_content = render_to_string('biomed_app/emails/expo_booking_update.html', context)
        text_content = strip_tags(html_content)
        try:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [booking.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=False)
            messages.success(request, f'Meeting request from {booking.name} rejected and email sent.')
        except Exception as e:
            print(f'Error sending meeting rejection email: {e}')
            messages.warning(request, f'Meeting request from {booking.name} rejected, but failed to send email.')
    else:
        messages.info(request, f'Meeting request from {booking.name} is already rejected.')
    return redirect('dashboard_expo_meeting_bookings')
'''

create_code = '''
@login_required(login_url='dashboard_login')
def exhibition_event_create(request):
    if request.method == 'POST':
        form = ExhibitionEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            subscribers = EventSubscriber.objects.filter(is_active=True)
            if subscribers.exists() and event.is_active:
                recipient_list = [sub.email for sub in subscribers]
                subject = f'Join us at {event.tag}!'
                
                context = {
                    'subject': subject,
                    'message': event.description,
                    'event_title': event.tag,
                    'event_date': event.event_date.strftime('%B %d, %Y') if event.event_date else '',
                    'event_location': event.location if hasattr(event, 'location') else ''
                }
                
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                html_content = render_to_string('biomed_app/emails/event_newsletter.html', context)
                text_content = strip_tags(html_content)
                try:
                    from django.core.mail import EmailMultiAlternatives
                    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, bcc=recipient_list)
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send(fail_silently=True)
                    messages.success(request, f'Event created and newsletter sent to {subscribers.count()} subscribers!')
                except Exception as e:
                    print(f'Error sending newsletter: {e}')
                    messages.warning(request, 'Event created, but failed to send newsletter to subscribers.')
            else:
                messages.success(request, 'Event created successfully!')
            return redirect('dashboard_exhibition_events')
    else:
        form = ExhibitionEventForm()
    return render(request, 'biomed_app/dashboard/exhibition_event_form.html', {'form': form, 'title': 'Add Exhibition Event'})
'''

print(replace_function(path, 'expo_meeting_booking_accept', accept_code))
print(replace_function(path, 'expo_meeting_booking_reject', reject_code))
print(replace_function(path, 'exhibition_event_create', create_code))
