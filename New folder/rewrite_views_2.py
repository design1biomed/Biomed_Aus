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

book_expo_code = '''
def book_expo_meeting(request, expo_id=None):
    initial_data = {}
    if expo_id:
        expo = get_object_or_404(ExhibitionEvent, pk=expo_id)
        initial_data['expo'] = expo
    if request.method == 'POST':
        form = ExpoMeetingBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Email to user
            subject = f'Meeting Request Received: {booking.expo.tag}'
            context_user = {
                'name': booking.name,
                'event_title': booking.expo.tag,
                'date': booking.meeting_date.strftime('%B %d, %Y') if booking.meeting_date else 'TBD',
                'time': booking.meeting_time.strftime('%I:%M %p') if booking.meeting_time else 'TBD'
            }
            user_html_content = render_to_string('biomed_app/emails/expo_booking_user.html', context_user)
            user_text_content = strip_tags(user_html_content)
            try:
                from django.core.mail import EmailMultiAlternatives
                msg_user = EmailMultiAlternatives(subject, user_text_content, settings.DEFAULT_FROM_EMAIL, [booking.email])
                msg_user.attach_alternative(user_html_content, 'text/html')
                msg_user.send(fail_silently=True)
            except Exception as e:
                print(f'Error sending meeting confirmation email: {e}')
                
            # Email to admin
            design_subject = f'New Meeting Request: {booking.name} at {booking.expo.tag}'
            site_url = request.build_absolute_uri('/')[:-1]
            from django.core.signing import Signer
            signer = Signer()
            signed_pk = signer.sign(booking.id)
            context_admin = {
                'name': booking.name,
                'email': booking.email,
                'phone': booking.phone or 'N/A',
                'company': booking.company_name or 'N/A',
                'event_title': booking.expo.tag,
                'date': booking.meeting_date.strftime('%B %d, %Y') if booking.meeting_date else 'TBD',
                'time': booking.meeting_time.strftime('%I:%M %p') if booking.meeting_time else 'TBD',
                'notes': booking.discussion_topics or 'No specific topics provided.'
            }
            design_html_content = render_to_string('biomed_app/emails/expo_booking_admin.html', context_admin)
            design_text_content = strip_tags(design_html_content)
            try:
                from django.core.mail import EmailMultiAlternatives
                from biomed_app.models import EmailConfiguration
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.booking_email if email_config and email_config.booking_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                msg_admin = EmailMultiAlternatives(design_subject, design_text_content, settings.DEFAULT_FROM_EMAIL, recipient_emails)
                msg_admin.attach_alternative(design_html_content, 'text/html')
                msg_admin.send(fail_silently=True)
            except Exception as e:
                print(f'Error sending meeting notification to design team: {e}')
            messages.success(request, 'Your meeting request has been submitted successfully! We have sent a confirmation email to your address.')
            return redirect(request.META.get('HTTP_REFERER', 'news_events'))
    else:
        form = ExpoMeetingBookingForm(initial=initial_data)
    import datetime
    import json
    expos = ExhibitionEvent.objects.filter(is_active=True)
    expo_dates = {}
    for e in expos:
        if e.event_date:
            dates = []
            current_date = e.event_date
            end_date = e.event_end_date or e.event_date
            while current_date <= end_date:
                dates.append({'value': current_date.strftime('%Y-%m-%d'), 'text': current_date.strftime('%d %B %Y')})
                current_date += datetime.timedelta(days=1)
            expo_dates[e.id] = dates
    booked_times = {}
    for e in expos:
        expo_id_str = str(e.id)
        booked_times[expo_id_str] = {}
        for b in e.meeting_bookings.exclude(status='rejected'):
            if b.meeting_date and b.meeting_time:
                d_str = b.meeting_date.strftime('%Y-%m-%d')
                t_str = b.meeting_time.strftime('%H:%M')
                if d_str not in booked_times[expo_id_str]:
                    booked_times[expo_id_str][d_str] = []
                booked_times[expo_id_str][d_str].append(t_str)
    return render(request, 'biomed_app/book_expo_meeting.html', {'form': form, 'expo_dates_json': json.dumps(expo_dates), 'booked_times_json': json.dumps(booked_times)})
'''

accept_code = '''
def public_expo_meeting_accept(request, signed_pk):
    from django.core.signing import Signer, BadSignature
    from django.http import HttpResponseBadRequest
    signer = Signer()
    try:
        pk = signer.unsign(signed_pk)
    except BadSignature:
        return HttpResponseBadRequest('Invalid or expired link.')
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
        html_content = render_to_string('biomed_app/emails/expo_booking_update.html', context)
        text_content = strip_tags(html_content)
        try:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [booking.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=True)
        except Exception as e:
            print(f'Error sending meeting acceptance email: {e}')
            
        # Admin confirmation
        admin_subject = f'Success: Meeting with {booking.name} Accepted'
        admin_message = f'You have successfully accepted the meeting request from {booking.name} for {booking.expo.tag}.'
        try:
            from biomed_app.models import EmailConfiguration
            email_config = EmailConfiguration.objects.first()
            email_str = email_config.booking_email if email_config and email_config.booking_email else 'design1@biomedingredients.com'
            recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
            from django.core.mail import send_mail
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=True)
        except Exception:
            pass
        return render(request, 'biomed_app/simple_action_success.html', {'message': f'Meeting request from {booking.name} has been accepted.', 'already_processed': False})
    else:
        return render(request, 'biomed_app/simple_action_success.html', {'message': f'Meeting request from {booking.name} was already accepted.', 'already_processed': True})
'''

reject_code = '''
def public_expo_meeting_reject(request, signed_pk):
    from django.core.signing import Signer, BadSignature
    from django.http import HttpResponseBadRequest
    signer = Signer()
    try:
        pk = signer.unsign(signed_pk)
    except BadSignature:
        return HttpResponseBadRequest('Invalid or expired link.')
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
        html_content = render_to_string('biomed_app/emails/expo_booking_update.html', context)
        text_content = strip_tags(html_content)
        try:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [booking.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=True)
        except Exception as e:
            print(f'Error sending meeting rejection email: {e}')
            
        # Admin confirmation
        admin_subject = f'Success: Meeting with {booking.name} Rejected'
        admin_message = f'You have successfully rejected the meeting request from {booking.name} for {booking.expo.tag}.'
        try:
            from biomed_app.models import EmailConfiguration
            email_config = EmailConfiguration.objects.first()
            email_str = email_config.booking_email if email_config and email_config.booking_email else 'design1@biomedingredients.com'
            recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
            from django.core.mail import send_mail
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=True)
        except Exception:
            pass
        return render(request, 'biomed_app/simple_action_success.html', {'message': f'Meeting request from {booking.name} has been rejected.', 'already_processed': False})
    else:
        return render(request, 'biomed_app/simple_action_success.html', {'message': f'Meeting request from {booking.name} was already rejected.', 'already_processed': True})
'''

print(replace_function(path, 'book_expo_meeting', book_expo_code))
print(replace_function(path, 'public_expo_meeting_accept', accept_code))
print(replace_function(path, 'public_expo_meeting_reject', reject_code))
