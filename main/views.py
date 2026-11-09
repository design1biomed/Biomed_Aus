from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import IndexPageContent, Accreditation, QualityTimeline, ExtractCategory, CorePromise, OfficeLocation, Enquiry, SolutionFeature, AboutPageContent, CSRPageContent, TeamMember, OperationTeamMember, InfrastructurePageContent, ResearchArea, ResearchCoreAreaLink, GalleryImage, Brand, ProductRangeSlide, Product, NaturalFoodColor, NaturalFlavour, ProductBrochure, ProductDocumentCategory, ProductDocument, ExhibitionEvent, EventSubscriber, InstagramPost, JobOpening, JobApplication, ContactMessage, EmailConfiguration, ExpoMeetingBooking
from .forms import IndexPageForm, AccreditationForm, QualityTimelineForm, ExtractCategoryForm, CorePromiseForm, OfficeLocationForm, SolutionFeatureForm, AboutPageForm, CSRPageForm, TeamMemberForm, OperationTeamMemberForm, InfrastructurePageForm, ResearchAreaForm, ResearchCoreAreaLinkForm, GalleryImageForm, BrandForm, ProductRangeSlideForm, ProductForm, NaturalFoodColorForm, NaturalFlavourForm, ProductBrochureForm, ProductDocumentCategoryForm, ProductDocumentForm, ExhibitionEventForm, InstagramPostForm, JobOpeningForm, JobApplicationForm, ContactMessageForm, EmailConfigurationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    content = IndexPageContent.load()
    accreditations = Accreditation.objects.all()
    timelines = QualityTimeline.objects.all()
    extracts = ExtractCategory.objects.all()
    promises = CorePromise.objects.all()
    offices = OfficeLocation.objects.all()
    features = SolutionFeature.objects.all()
    return render(request, 'main/index.html', {
        'content': content, 
        'accreditations': accreditations, 
        'timelines': timelines, 
        'extracts': extracts,
        'promises': promises,
        'offices': offices,
        'features': features,
    })

def accreditations_page(request):
    accreditations_list = Accreditation.objects.all()
    # Simple session check for unlocking PDFs
    access_granted = request.session.get('accreditations_unlocked', False)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if name and email:
            # Unlock the PDFs for this user session
            request.session['accreditations_unlocked'] = True
            access_granted = True
            messages.success(request, 'Thank you! You now have access to view our accreditation documents.')
            
    return render(request, 'main/accreditations.html', {
        'accreditations_list': accreditations_list,
        'access_granted': access_granted
    })

def facility_page(request):
    return render(request, 'main/facility.html')

def research_page(request):
    query = request.GET.get('q', '')
    
    if query:
        areas = ResearchArea.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        areas = ResearchArea.objects.all()
        
    core_areas = ResearchCoreAreaLink.objects.all()
    gallery_images = GalleryImage.objects.all()
    
    return render(request, 'main/research.html', {
        'areas': areas,
        'core_areas': core_areas,
        'gallery_images': gallery_images,
        'query': query,
    })

def research_area_detail(request, slug):
    area = get_object_or_404(ResearchArea, slug=slug)
    
    # We will pass the same sidebar variables just in case
    core_areas = ResearchCoreAreaLink.objects.all()
    gallery_images = GalleryImage.objects.all()
    
    return render(request, 'main/research_detail.html', {
        'area': area,
        'core_areas': core_areas,
        'gallery_images': gallery_images,
    })

@login_required(login_url='dashboard_login')
def custom_dashboard(request):
    from .models import (
        Product, ExhibitionEvent, ExpoMeetingBooking, Enquiry,
        ContactMessage, JobApplication, EventSubscriber
    )
    auto_sync_expired_exhibitions()
    total_leads = (
        Enquiry.objects.count() +
        ContactMessage.objects.count() +
        JobApplication.objects.count() +
        ExpoMeetingBooking.objects.count()
    )
    stats = {
        'products_count': Product.objects.count(),
        'exhibitions_count': ExhibitionEvent.objects.filter(is_active=True).count(),
        'expo_bookings_pending': ExpoMeetingBooking.objects.filter(status='pending').count(),
        'total_leads': total_leads,
        'enquiries_count': Enquiry.objects.count(),
        'contact_messages_count': ContactMessage.objects.count(),
        'job_applications_count': JobApplication.objects.count(),
        'subscribers_count': EventSubscriber.objects.count(),
    }
    return render(request, 'main/dashboard/dashboard.html', {'stats': stats})

@login_required(login_url='dashboard_login')
def edit_index_page(request):
    content = IndexPageContent.load()
    
    if request.method == 'POST':
        form = IndexPageForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Index page content updated successfully!')
            return redirect('custom_dashboard')
    else:
        form = IndexPageForm(instance=content)
        
    return render(request, 'main/dashboard/edit_index.html', {'form': form})

@login_required(login_url='dashboard_login')
def manage_accreditations(request):
    accreditations = Accreditation.objects.all()
    return render(request, 'main/dashboard/accreditations/list.html', {'accreditations': accreditations})

@login_required(login_url='dashboard_login')
def add_accreditation(request):
    if request.method == 'POST':
        form = AccreditationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accreditation added successfully!')
            return redirect('manage_accreditations')
    else:
        form = AccreditationForm()
    return render(request, 'main/dashboard/accreditations/form.html', {'form': form, 'title': 'Add Accreditation'})

@login_required(login_url='dashboard_login')
def edit_accreditation(request, pk):
    accreditation = Accreditation.objects.get(pk=pk)
    if request.method == 'POST':
        form = AccreditationForm(request.POST, request.FILES, instance=accreditation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accreditation updated successfully!')
            return redirect('manage_accreditations')
    else:
        form = AccreditationForm(instance=accreditation)
    return render(request, 'main/dashboard/accreditations/form.html', {'form': form, 'title': 'Edit Accreditation'})

@login_required(login_url='dashboard_login')
def delete_accreditation(request, pk):
    if request.method == 'POST':
        accred = Accreditation.objects.get(pk=pk)
        accred.delete()
        messages.success(request, 'Accreditation deleted successfully!')
    return redirect('manage_accreditations')

@login_required(login_url='dashboard_login')
def manage_timelines(request):
    timelines = QualityTimeline.objects.all()
    return render(request, 'main/dashboard/timelines/list.html', {'timelines': timelines})

@login_required(login_url='dashboard_login')
def add_timeline(request):
    if request.method == 'POST':
        form = QualityTimelineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quality timeline item added successfully!')
            return redirect('manage_timelines')
    else:
        form = QualityTimelineForm()
    return render(request, 'main/dashboard/timelines/form.html', {'form': form, 'title': 'Add Timeline Item'})

@login_required(login_url='dashboard_login')
def edit_timeline(request, pk):
    timeline = QualityTimeline.objects.get(pk=pk)
    if request.method == 'POST':
        form = QualityTimelineForm(request.POST, instance=timeline)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timeline item updated successfully!')
            return redirect('manage_timelines')
    else:
        form = QualityTimelineForm(instance=timeline)
    return render(request, 'main/dashboard/timelines/form.html', {'form': form, 'title': 'Edit Timeline Item'})

@login_required(login_url='dashboard_login')
def delete_timeline(request, pk):
    if request.method == 'POST':
        item = QualityTimeline.objects.get(pk=pk)
        item.delete()
        messages.success(request, 'Timeline item deleted successfully!')
    return redirect('manage_timelines')


@login_required(login_url='dashboard_login')
def manage_extracts(request):
    extracts = ExtractCategory.objects.all()
    return render(request, 'main/dashboard/extracts/list.html', {'extracts': extracts})

@login_required(login_url='dashboard_login')
def add_extract(request):
    if request.method == 'POST':
        form = ExtractCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Extract category added successfully!')
            return redirect('manage_extracts')
    else:
        form = ExtractCategoryForm()
    return render(request, 'main/dashboard/extracts/form.html', {'form': form, 'title': 'Add Extract Category'})

@login_required(login_url='dashboard_login')
def edit_extract(request, pk):
    extract = ExtractCategory.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExtractCategoryForm(request.POST, request.FILES, instance=extract)
        if form.is_valid():
            form.save()
            messages.success(request, 'Extract category updated successfully!')
            return redirect('manage_extracts')
    else:
        form = ExtractCategoryForm(instance=extract)
    return render(request, 'main/dashboard/extracts/form.html', {'form': form, 'title': 'Edit Extract Category'})

@login_required(login_url='dashboard_login')
def delete_extract(request, pk):
    if request.method == 'POST':
        extract = ExtractCategory.objects.get(pk=pk)
        extract.delete()
        messages.success(request, 'Extract category deleted successfully!')
    return redirect('manage_extracts')

@login_required(login_url='dashboard_login')
def manage_promises(request):
    promises = CorePromise.objects.all()
    return render(request, 'main/dashboard/promises/list.html', {'promises': promises})

@login_required(login_url='dashboard_login')
def add_promise(request):
    if request.method == 'POST':
        form = CorePromiseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Core Promise added successfully!')
            return redirect('manage_promises')
    else:
        form = CorePromiseForm()
    return render(request, 'main/dashboard/promises/form.html', {'form': form, 'title': 'Add Core Promise'})

@login_required(login_url='dashboard_login')
def edit_promise(request, pk):
    promise = CorePromise.objects.get(pk=pk)
    if request.method == 'POST':
        form = CorePromiseForm(request.POST, instance=promise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Core Promise updated successfully!')
            return redirect('manage_promises')
    else:
        form = CorePromiseForm(instance=promise)
    return render(request, 'main/dashboard/promises/form.html', {'form': form, 'title': 'Edit Core Promise'})

@login_required(login_url='dashboard_login')
def delete_promise(request, pk):
    if request.method == 'POST':
        promise = CorePromise.objects.get(pk=pk)
        promise.delete()
        messages.success(request, 'Core Promise deleted successfully!')
    return redirect('manage_promises')

@login_required(login_url='dashboard_login')
def manage_offices(request):
    offices = OfficeLocation.objects.all()
    return render(request, 'main/dashboard/offices/list.html', {'offices': offices})

@login_required(login_url='dashboard_login')
def add_office(request):
    if request.method == 'POST':
        form = OfficeLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Office location added successfully!')
            return redirect('manage_offices')
    else:
        form = OfficeLocationForm()
    return render(request, 'main/dashboard/offices/form.html', {'form': form, 'title': 'Add Office Location'})

@login_required(login_url='dashboard_login')
def edit_office(request, pk):
    office = OfficeLocation.objects.get(pk=pk)
    if request.method == 'POST':
        form = OfficeLocationForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, 'Office location updated successfully!')
            return redirect('manage_offices')
    else:
        form = OfficeLocationForm(instance=office)
    return render(request, 'main/dashboard/offices/form.html', {'form': form, 'title': 'Edit Office Location'})

@login_required(login_url='dashboard_login')
def delete_office(request, pk):
    if request.method == 'POST':
        office = OfficeLocation.objects.get(pk=pk)
        office.delete()
        messages.success(request, 'Office location deleted successfully!')
    return redirect('manage_offices')

@login_required(login_url='dashboard_login')
def manage_solutions(request):
    features = SolutionFeature.objects.all()
    return render(request, 'main/dashboard/solutions/list.html', {'features': features})

@login_required(login_url='dashboard_login')
def add_solution(request):
    if request.method == 'POST':
        form = SolutionFeatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solution feature added successfully!')
            return redirect('manage_solutions')
    else:
        form = SolutionFeatureForm()
    return render(request, 'main/dashboard/solutions/form.html', {'form': form, 'title': 'Add Solution Feature'})

@login_required(login_url='dashboard_login')
def edit_solution(request, pk):
    feature = SolutionFeature.objects.get(pk=pk)
    if request.method == 'POST':
        form = SolutionFeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solution feature updated successfully!')
            return redirect('manage_solutions')
    else:
        form = SolutionFeatureForm(instance=feature)
    return render(request, 'main/dashboard/solutions/form.html', {'form': form, 'title': 'Edit Solution Feature'})

@login_required(login_url='dashboard_login')
def delete_solution(request, pk):
    if request.method == 'POST':
        feature = SolutionFeature.objects.get(pk=pk)
        feature.delete()
        messages.success(request, 'Solution feature deleted successfully!')
    return redirect('manage_solutions')

@login_required(login_url='dashboard_login')
def manage_enquiries(request):
    enquiries = Enquiry.objects.all()
    return render(request, 'main/dashboard/enquiries/list.html', {'enquiries': enquiries})

@login_required(login_url='dashboard_login')
def delete_enquiry(request, pk):
    if request.method == 'POST':
        enquiry = Enquiry.objects.get(pk=pk)
        enquiry.delete()
        messages.success(request, 'Enquiry deleted successfully!')
    return redirect('manage_enquiries')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def submit_enquiry(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        company = request.POST.get('company')
        email = request.POST.get('email')
        product_name = request.POST.get('product_name')
        message = request.POST.get('message')
        
        Enquiry.objects.create(
            full_name=full_name,
            company=company,
            email=email,
            product_name=product_name,
            message=message
        )
        
        try:
            from django.core.mail import EmailMessage
            from django.conf import settings
            from django.template.loader import render_to_string
            
            email_config = EmailConfiguration.objects.first()
            email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
            recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
            
            subject = f"New Enquiry from {full_name}"
            
            html_message = render_to_string('main/email/general_email.html', {
                'title': 'New Product Enquiry',
                'intro_text': 'A new product enquiry has been submitted from the website.',
                'details': {
                    'Name': full_name,
                    'Company': company,
                    'Email': email,
                    'Product': product_name,
                    'Message': message
                }
            })
            
            msg = EmailMessage(
                subject,
                html_message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                recipient_emails
            )
            msg.content_subtype = "html"
            msg.send(fail_silently=True)
        except Exception:
            pass
            
        messages.success(request, 'Thank you! Your enquiry has been submitted. Our team will contact you shortly.')
        return redirect('submit_enquiry')
    
    # Handle GET Request (Render the dedicated page)
    product_name = request.GET.get('product', '')
    return render(request, 'main/enquiry.html', {'product_name': product_name})

@csrf_exempt
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('custom_dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('custom_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'main/dashboard/login.html')

def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')

def about_us(request):
    content = AboutPageContent.load()
    return render(request, 'main/about.html', {'content': content})

@login_required(login_url='dashboard_login')
def edit_about_page(request):
    content = AboutPageContent.load()
    
    if request.method == 'POST':
        form = AboutPageForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'About page content updated successfully!')
            return redirect('custom_dashboard')
    else:
        form = AboutPageForm(instance=content)
        
    return render(request, 'main/dashboard/edit_about.html', {'form': form})

def csr_page(request):
    content = CSRPageContent.load()
    return render(request, 'main/csr.html', {'content': content})

@login_required(login_url='dashboard_login')
def edit_csr_page(request):
    content = CSRPageContent.load()
    
    if request.method == 'POST':
        form = CSRPageForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'CSR page content updated successfully!')
            return redirect('custom_dashboard')
    else:
        form = CSRPageForm(instance=content)
        
    return render(request, 'main/dashboard/edit_csr.html', {'form': form})


def team_page(request):
    team_members = TeamMember.objects.all()
    operation_members = OperationTeamMember.objects.all()
    return render(request, 'main/team.html', {
        'team_members': team_members,
        'operation_members': operation_members
    })

@login_required(login_url='dashboard_login')
def manage_team(request):
    team_members = TeamMember.objects.all()
    operation_members = OperationTeamMember.objects.all()
    return render(request, 'main/dashboard/manage_team.html', {
        'team_members': team_members,
        'operation_members': operation_members
    })

from django.shortcuts import get_object_or_404

@login_required(login_url='dashboard_login')
def add_team_member(request, team_type):
    if team_type == 'core':
        form_class = TeamMemberForm
        title = "Add Core Team Member"
    else:
        form_class = OperationTeamMemberForm
        title = "Add Operation Team Member"
        
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('manage_team')
    else:
        form = form_class()
        
    return render(request, 'main/dashboard/edit_team_member.html', {'form': form, 'title': title})

@login_required(login_url='dashboard_login')
def edit_team_member(request, team_type, pk):
    if team_type == 'core':
        member = get_object_or_404(TeamMember, pk=pk)
        form_class = TeamMemberForm
        title = "Edit Core Team Member"
    else:
        member = get_object_or_404(OperationTeamMember, pk=pk)
        form_class = OperationTeamMemberForm
        title = "Edit Operation Team Member"
        
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('manage_team')
    else:
        form = form_class(instance=member)
        
    return render(request, 'main/dashboard/edit_team_member.html', {'form': form, 'title': title})

@login_required(login_url='dashboard_login')
def delete_team_member(request, team_type, pk):
    if team_type == 'core':
        member = get_object_or_404(TeamMember, pk=pk)
    else:
        member = get_object_or_404(OperationTeamMember, pk=pk)
        
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted successfully!')
        
    return redirect('manage_team')

def infrastructure_page(request):
    content = InfrastructurePageContent.load()
    features = SolutionFeature.objects.all()
    # Split features into left and right columns
    mid = len(features) // 2
    features_left = features[:mid] if len(features) > 0 else []
    features_right = features[mid:] if len(features) > 0 else []
    
    return render(request, 'main/infrastructure_services.html', {
        'content': content,
        'features_left': features_left,
        'features_right': features_right
    })

@login_required(login_url='dashboard_login')
def edit_infrastructure_page(request):
    content = InfrastructurePageContent.load()
    if request.method == 'POST':
        form = InfrastructurePageForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()

def infrastructure_page(request):
    content = InfrastructurePageContent.load()
    features = SolutionFeature.objects.all()
    # Split features into left and right columns
    mid = len(features) // 2
    features_left = features[:mid] if len(features) > 0 else []
    features_right = features[mid:] if len(features) > 0 else []
    
    return render(request, 'main/infrastructure_services.html', {
        'content': content,
        'features_left': features_left,
        'features_right': features_right
    })

@login_required(login_url='dashboard_login')
def edit_infrastructure_page(request):
    content = InfrastructurePageContent.load()
    if request.method == 'POST':
        form = InfrastructurePageForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Infrastructure & Services page updated successfully.')
            return redirect('edit_infrastructure_page')
    else:
        form = InfrastructurePageForm(instance=content)
        
    return render(request, 'main/dashboard/edit_infrastructure.html', {'form': form})

# --- Research Page Dashboard ---

@login_required(login_url='dashboard_login')
def manage_research(request):
    areas = ResearchArea.objects.all()
    core_links = ResearchCoreAreaLink.objects.all()
    gallery = GalleryImage.objects.all()
    return render(request, 'main/dashboard/manage_research.html', {
        'areas': areas,
        'core_links': core_links,
        'gallery': gallery,
    })

@login_required(login_url='dashboard_login')
def add_research_area(request):
    if request.method == 'POST':
        form = ResearchAreaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research Area added successfully.')
            return redirect('manage_research')
    else:
        form = ResearchAreaForm()
    return render(request, 'main/dashboard/edit_research_area.html', {'form': form, 'title': 'Add Research Area'})

@login_required(login_url='dashboard_login')
def edit_research_area(request, pk):
    area = get_object_or_404(ResearchArea, pk=pk)
    if request.method == 'POST':
        form = ResearchAreaForm(request.POST, request.FILES, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research Area updated successfully.')
            return redirect('manage_research')
    else:
        form = ResearchAreaForm(instance=area)
    return render(request, 'main/dashboard/edit_research_area.html', {'form': form, 'title': 'Edit Research Area'})

@login_required(login_url='dashboard_login')
def delete_research_area(request, pk):
    area = get_object_or_404(ResearchArea, pk=pk)
    if request.method == 'POST':
        area.delete()
        messages.success(request, 'Research Area deleted successfully.')
        return redirect('manage_research')
    return redirect('manage_research')

@login_required(login_url='dashboard_login')
def add_core_link(request):
    if request.method == 'POST':
        form = ResearchCoreAreaLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Core Area Link added successfully.')
            return redirect('manage_research')
    else:
        form = ResearchCoreAreaLinkForm()
    research_areas = ResearchArea.objects.all()
    return render(request, 'main/dashboard/edit_core_link.html', {'form': form, 'title': 'Add Core Area Link', 'research_areas': research_areas})

@login_required(login_url='dashboard_login')
def edit_core_link(request, pk):
    link = get_object_or_404(ResearchCoreAreaLink, pk=pk)
    if request.method == 'POST':
        form = ResearchCoreAreaLinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, 'Core Area Link updated successfully.')
            return redirect('manage_research')
    else:
        form = ResearchCoreAreaLinkForm(instance=link)
    research_areas = ResearchArea.objects.all()
    return render(request, 'main/dashboard/edit_core_link.html', {'form': form, 'title': 'Edit Core Area Link', 'research_areas': research_areas})

@login_required(login_url='dashboard_login')
def delete_core_link(request, pk):
    link = get_object_or_404(ResearchCoreAreaLink, pk=pk)
    if request.method == 'POST':
        link.delete()
        messages.success(request, 'Core Area Link deleted successfully.')
        return redirect('manage_research')
    return redirect('manage_research')

@login_required(login_url='dashboard_login')
def add_gallery_image(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery Image added successfully.')
            return redirect('manage_research')
    else:
        form = GalleryImageForm()
    return render(request, 'main/dashboard/edit_gallery_image.html', {'form': form, 'title': 'Add Gallery Image'})

@login_required(login_url='dashboard_login')
def edit_gallery_image(request, pk):
    img = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery Image updated successfully.')
            return redirect('manage_research')
    else:
        form = GalleryImageForm(instance=img)
    return render(request, 'main/dashboard/edit_gallery_image.html', {'form': form, 'title': 'Edit Gallery Image'})

@login_required(login_url='dashboard_login')
def delete_gallery_image(request, pk):
    img = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        img.delete()
        messages.success(request, 'Gallery Image deleted successfully.')
        return redirect('manage_research')
    return redirect('manage_research')

# ==========================================
# Brands / Trademarks Views
# ==========================================

def brands_list(request):
    brands = Brand.objects.all()
    return render(request, 'main/brands.html', {'brands_list': brands})

def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    related_brands = Brand.objects.exclude(pk=brand.pk)[:4]
    return render(request, 'main/brand_detail.html', {'brand': brand, 'related_brands': related_brands})

@login_required(login_url='dashboard_login')
def dashboard_manage_brands(request):
    brands = Brand.objects.all()
    return render(request, 'main/dashboard/manage_brands.html', {'brands': brands})

@login_required(login_url='dashboard_login')
def dashboard_add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully.')
            return redirect('dashboard_manage_brands')
    else:
        form = BrandForm()
    return render(request, 'main/dashboard/edit_brand.html', {'form': form, 'title': 'Add Brand', 'is_update': False})

@login_required(login_url='dashboard_login')
def dashboard_edit_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully.')
            return redirect('dashboard_manage_brands')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'main/dashboard/edit_brand.html', {'form': form, 'title': 'Edit Brand', 'is_update': True})

@login_required(login_url='dashboard_login')
def dashboard_delete_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted successfully.')
        return redirect('dashboard_manage_brands')
    return render(request, 'main/dashboard/delete_confirm.html', {'object': brand, 'type': 'Brand', 'cancel_url': 'dashboard_manage_brands'})

# ==========================================
# PRODUCT RANGE VIEWS
# ==========================================
def product_range(request):
    slides = ProductRangeSlide.objects.all()
    return render(request, 'main/product_range.html', {'slides': slides})

@login_required(login_url='dashboard_login')
def dashboard_manage_product_range(request):
    slides = ProductRangeSlide.objects.all()
    return render(request, 'main/dashboard/manage_product_range.html', {'slides': slides})

@login_required(login_url='dashboard_login')
def dashboard_add_product_range(request):
    if request.method == 'POST':
        form = ProductRangeSlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product range slide added successfully.')
            return redirect('dashboard_manage_product_range')
    else:
        form = ProductRangeSlideForm()
    return render(request, 'main/dashboard/edit_product_range.html', {'form': form, 'title': 'Add Product Range Slide'})

@login_required(login_url='dashboard_login')
def dashboard_edit_product_range(request, pk):
    slide = get_object_or_404(ProductRangeSlide, pk=pk)
    if request.method == 'POST':
        form = ProductRangeSlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product range slide updated successfully.')
            return redirect('dashboard_manage_product_range')
    else:
        form = ProductRangeSlideForm(instance=slide)
    return render(request, 'main/dashboard/edit_product_range.html', {'form': form, 'title': 'Edit Product Range Slide', 'is_update': True})

@login_required(login_url='dashboard_login')
def dashboard_delete_product_range(request, pk):
    slide = get_object_or_404(ProductRangeSlide, pk=pk)
    if request.method == 'POST':
        slide.delete()
        messages.success(request, 'Product range slide deleted successfully!')
        return redirect('dashboard_manage_product_range')
    return render(request, 'main/dashboard/delete_product_range.html', {'slide': slide})

def herbal_extracts(request):
    all_products = Product.objects.all().order_by('category', 'name')
    
    # Group products by their category display name
    from collections import OrderedDict
    grouped = OrderedDict()
    for prod in all_products:
        label = prod.get_category_display()
        if label not in grouped:
            grouped[label] = []
        grouped[label].append(prod)
        
    return render(request, "main/herbal_extracts.html", {
        "products": all_products,
        "grouped_products": grouped,
    })

# --- Product Dashboard Views ---
@login_required(login_url='dashboard_login')
def dashboard_manage_products(request):
    category = request.GET.get('category', None)
    if category:
        products = Product.objects.filter(category=category).order_by('name')
        # Create a display title from the category slug
        page_title = category.replace('_', ' ').title()
    else:
        products = Product.objects.all().order_by('category', 'name')
        page_title = 'All Products'
    return render(request, 'main/dashboard/manage_products.html', {'products': products, 'current_category': category, 'page_title': page_title})

from django.urls import reverse

@login_required(login_url='dashboard_login')
def dashboard_add_product(request):
    category = request.GET.get('category', None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            url = reverse('dashboard_manage_products')
            if category:
                url += f'?category={category}'
            return redirect(url)
    else:
        initial_data = {}
        if category:
            initial_data['category'] = category
        form = ProductForm(initial=initial_data)
    return render(request, 'main/dashboard/edit_product.html', {'form': form, 'title': 'Add Product', 'current_category': category})

@login_required(login_url='dashboard_login')
def dashboard_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category = request.GET.get('category', None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            url = reverse('dashboard_manage_products')
            if category:
                url += f'?category={category}'
            return redirect(url)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/dashboard/edit_product.html', {'form': form, 'title': 'Edit Product', 'product': product, 'current_category': category})

@login_required(login_url='dashboard_login')
def dashboard_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category = request.GET.get('category', None)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        url = reverse('dashboard_manage_products')
        if category:
            url += f'?category={category}'
        return redirect(url)
    return render(request, 'main/dashboard/delete_product.html', {'product': product, 'current_category': category})

# --- Natural Food Colors Front-end View ---
def natural_food_colors(request):
    colors = NaturalFoodColor.objects.all().order_by('order', 'id')
    flavours = NaturalFlavour.objects.all().order_by('category', 'order', 'id')
    
    from collections import OrderedDict
    grouped_flavours = OrderedDict()
    for flavour in flavours:
        cat = flavour.category or "Other"
        if cat not in grouped_flavours:
            grouped_flavours[cat] = []
        grouped_flavours[cat].append(flavour)
    return render(request, "main/natural_food_colors.html", {
        "colors": colors,
        "grouped_flavours": grouped_flavours
    })

# --- Dashboard: Natural Food Colors ---
@login_required(login_url='dashboard_login')
def dashboard_manage_natural_food_colors(request):
    colors = NaturalFoodColor.objects.all().order_by('order', 'id')
    return render(request, 'main/dashboard/manage_natural_food_colors.html', {'colors': colors})

@login_required(login_url='dashboard_login')
def dashboard_add_natural_food_color(request):
    if request.method == 'POST':
        form = NaturalFoodColorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Natural Food Color added successfully!')
            return redirect('dashboard_manage_natural_food_colors')
    else:
        form = NaturalFoodColorForm()
    return render(request, 'main/dashboard/edit_natural_food_color.html', {'form': form, 'title': 'Add Natural Food Color'})

@login_required(login_url='dashboard_login')
def dashboard_edit_natural_food_color(request, pk):
    color = get_object_or_404(NaturalFoodColor, pk=pk)
    if request.method == 'POST':
        form = NaturalFoodColorForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            messages.success(request, 'Natural Food Color updated successfully!')
            return redirect('dashboard_manage_natural_food_colors')
    else:
        form = NaturalFoodColorForm(instance=color)
    return render(request, 'main/dashboard/edit_natural_food_color.html', {'form': form, 'title': 'Edit Natural Food Color', 'color': color})

@login_required(login_url='dashboard_login')
def dashboard_delete_natural_food_color(request, pk):
    color = get_object_or_404(NaturalFoodColor, pk=pk)
    if request.method == 'POST':
        color.delete()
        messages.success(request, 'Natural Food Color deleted successfully!')
        return redirect('dashboard_manage_natural_food_colors')
    return render(request, 'main/dashboard/delete_natural_food_color.html', {'color': color})


# --- Dashboard: Natural Flavours ---
@login_required(login_url='dashboard_login')
def dashboard_manage_natural_flavours(request):
    flavours = NaturalFlavour.objects.all().order_by('category', 'order', 'id')
    return render(request, 'main/dashboard/manage_natural_flavours.html', {'flavours': flavours})

@login_required(login_url='dashboard_login')
def dashboard_add_natural_flavour(request):
    if request.method == 'POST':
        form = NaturalFlavourForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Natural Flavour added successfully!')
            return redirect('dashboard_manage_natural_flavours')
    else:
        form = NaturalFlavourForm()
    return render(request, 'main/dashboard/edit_natural_flavour.html', {'form': form, 'title': 'Add Natural Flavour'})

@login_required(login_url='dashboard_login')
def dashboard_edit_natural_flavour(request, pk):
    flavour = get_object_or_404(NaturalFlavour, pk=pk)
    if request.method == 'POST':
        form = NaturalFlavourForm(request.POST, instance=flavour)
        if form.is_valid():
            form.save()
            messages.success(request, 'Natural Flavour updated successfully!')
            return redirect('dashboard_manage_natural_flavours')
    else:
        form = NaturalFlavourForm(instance=flavour)
    return render(request, 'main/dashboard/edit_natural_flavour.html', {'form': form, 'title': 'Edit Natural Flavour', 'flavour': flavour})

@login_required(login_url='dashboard_login')
def dashboard_delete_natural_flavour(request, pk):
    flavour = get_object_or_404(NaturalFlavour, pk=pk)
    if request.method == 'POST':
        flavour.delete()
        messages.success(request, 'Natural Flavour deleted successfully!')
        return redirect('dashboard_manage_natural_flavours')
    return render(request, 'main/dashboard/delete_natural_flavour.html', {'flavour': flavour})

# --- Product Brochures Front-end View ---
def product_brochures(request):
    brochures = ProductBrochure.objects.all().order_by('order', 'id')
    return render(request, "main/product_brochures.html", {"brochures": brochures})

# --- Dashboard: Product Brochures ---
@login_required(login_url='dashboard_login')
def dashboard_manage_product_brochures(request):
    brochures = ProductBrochure.objects.all().order_by('order', 'id')
    return render(request, 'main/dashboard/manage_product_brochures.html', {'brochures': brochures})

@login_required(login_url='dashboard_login')
def dashboard_add_product_brochure(request):
    if request.method == 'POST':
        form = ProductBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Brochure added successfully!')
            return redirect('dashboard_manage_product_brochures')
    else:
        form = ProductBrochureForm()
    return render(request, 'main/dashboard/edit_product_brochure.html', {'form': form, 'title': 'Add Product Brochure'})

@login_required(login_url='dashboard_login')
def dashboard_edit_product_brochure(request, pk):
    brochure = get_object_or_404(ProductBrochure, pk=pk)
    if request.method == 'POST':
        form = ProductBrochureForm(request.POST, request.FILES, instance=brochure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Brochure updated successfully!')
            return redirect('dashboard_manage_product_brochures')
    else:
        form = ProductBrochureForm(instance=brochure)
    return render(request, 'main/dashboard/edit_product_brochure.html', {'form': form, 'title': 'Edit Product Brochure', 'brochure': brochure})

@login_required(login_url='dashboard_login')
def dashboard_delete_product_brochure(request, pk):
    brochure = get_object_or_404(ProductBrochure, pk=pk)
    if request.method == 'POST':
        brochure.delete()
        messages.success(request, 'Product Brochure deleted successfully!')
        return redirect('dashboard_manage_product_brochures')
    return render(request, 'main/dashboard/delete_product_brochure.html', {'brochure': brochure})

# --- Product Documents Front-end View ---
def product_documents(request):
    categories = ProductDocumentCategory.objects.all().prefetch_related('product_documents')
    documents_raw = ProductDocument.objects.all().select_related('category').order_by('category__name', 'name')
    
    documents = []
    for doc in documents_raw:
        pdf_list = []
        if doc.pdfs:
            raw_paths = [p.strip() for p in doc.pdfs.split(',') if p.strip()]
            for path in raw_paths:
                filename = path.split('/')[-1]
                title = filename.replace('-', ' ').replace('_', ' ').replace('.pdf', '').title()
                pdf_list.append({'title': title, 'path': path})
                
        documents.append({
            'id': doc.id,
            'name': doc.name,
            'category_name': doc.category.name if doc.category else "Uncategorized",
            'image': doc.image,
            'pdfs': pdf_list
        })

    return render(request, "main/product_documents.html", {
        "categories": categories,
        "documents": documents
    })

# --- Dashboard: Product Document Categories ---
@login_required(login_url='dashboard_login')
def dashboard_manage_product_document_categories(request):
    categories = ProductDocumentCategory.objects.all()
    return render(request, 'main/dashboard/manage_product_document_categories.html', {'categories': categories})

@login_required(login_url='dashboard_login')
def dashboard_add_product_document_category(request):
    if request.method == 'POST':
        form = ProductDocumentCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard_manage_product_document_categories')
    else:
        form = ProductDocumentCategoryForm()
    return render(request, 'main/dashboard/edit_product_document_category.html', {'form': form, 'title': 'Add Category'})

@login_required(login_url='dashboard_login')
def dashboard_edit_product_document_category(request, pk):
    category = get_object_or_404(ProductDocumentCategory, pk=pk)
    if request.method == 'POST':
        form = ProductDocumentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('dashboard_manage_product_document_categories')
    else:
        form = ProductDocumentCategoryForm(instance=category)
    return render(request, 'main/dashboard/edit_product_document_category.html', {'form': form, 'title': 'Edit Category', 'category': category})

@login_required(login_url='dashboard_login')
def dashboard_delete_product_document_category(request, pk):
    category = get_object_or_404(ProductDocumentCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('dashboard_manage_product_document_categories')
    return render(request, 'main/dashboard/delete_product_document_category.html', {'category': category})

# --- Dashboard: Product Documents ---
@login_required(login_url='dashboard_login')
def dashboard_manage_product_documents(request):
    documents = ProductDocument.objects.all().select_related('category')
    return render(request, 'main/dashboard/manage_product_documents.html', {'documents': documents})

@login_required(login_url='dashboard_login')
def dashboard_add_product_document(request):
    if request.method == 'POST':
        form = ProductDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            
            # Get existing PDFs string (from hidden input if we are modifying it)
            existing_pdfs = doc.pdfs.split(',') if doc.pdfs else []
            existing_pdfs = [p.strip() for p in existing_pdfs if p.strip()]

            # Handle new PDF uploads
            pdf_files = request.FILES.getlist('pdf_files')
            for pdf in pdf_files:
                # Save file to media/product_documents/pdfs/
                file_name = default_storage.save(f'product_documents/pdfs/{pdf.name}', pdf)
                existing_pdfs.append(file_name)

            doc.pdfs = ','.join(existing_pdfs)
            doc.save()

            messages.success(request, 'Product Document added successfully!')
            return redirect('dashboard_manage_product_documents')
    else:
        form = ProductDocumentForm()
    return render(request, 'main/dashboard/edit_product_document.html', {'form': form, 'title': 'Add Product Document'})

@login_required(login_url='dashboard_login')
def dashboard_edit_product_document(request, pk):
    document = get_object_or_404(ProductDocument, pk=pk)
    if request.method == 'POST':
        form = ProductDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            
            # The frontend JS maintains the `doc.pdfs` textarea with the current list of kept PDFs
            existing_pdfs = doc.pdfs.split(',') if doc.pdfs else []
            existing_pdfs = [p.strip() for p in existing_pdfs if p.strip()]

            # Handle new PDF uploads
            pdf_files = request.FILES.getlist('pdf_files')
            for pdf in pdf_files:
                file_name = default_storage.save(f'product_documents/pdfs/{pdf.name}', pdf)
                existing_pdfs.append(file_name)

            doc.pdfs = ','.join(existing_pdfs)
            doc.save()

            messages.success(request, 'Product Document updated successfully!')
            return redirect('dashboard_manage_product_documents')
    else:
        form = ProductDocumentForm(instance=document)
    return render(request, 'main/dashboard/edit_product_document.html', {'form': form, 'title': 'Edit Product Document', 'document': document})

@login_required(login_url='dashboard_login')
def dashboard_delete_product_document(request, pk):
    document = get_object_or_404(ProductDocument, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Product Document deleted successfully!')
        return redirect('dashboard_manage_product_documents')
    return render(request, 'main/dashboard/delete_product_document.html', {'document': document})

# --- Auto-sync expired exhibitions ---
def auto_sync_expired_exhibitions():
    """
    Scans active ExhibitionEvent records and automatically deactivates (is_active = False)
    any event whose end date (or start date if no end date provided) has passed (< today).
    Returns the number of events newly marked inactive.
    """
    from datetime import date
    from django.db.models import Q
    today = date.today()
    expired_active = ExhibitionEvent.objects.filter(is_active=True).filter(
        Q(event_end_date__isnull=False, event_end_date__lt=today) |
        Q(event_end_date__isnull=True, event_date__isnull=False, event_date__lt=today)
    )
    count = expired_active.count()
    if count > 0:
        expired_active.update(is_active=False)
    return count

# --- News & Events Front-end View ---
def news_events(request):
    auto_sync_expired_exhibitions()
    instagram_posts = InstagramPost.objects.filter(is_visible=True)
    exhibitions = ExhibitionEvent.objects.filter(is_active=True).order_by('order', '-id')
    return render(request, "main/news_events.html", {
        "instagram_posts": instagram_posts,
        "exhibitions": exhibitions
    })

def subscribe_event_notifications(request):
    if request.method == "POST":
        email = request.POST.get("email")
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or
            request.headers.get('Accept') == 'application/json' or
            request.POST.get('is_ajax') == '1'
        )
        if email:
            subscriber, created = EventSubscriber.objects.get_or_create(email=email)
            if created:
                try:
                    from django.core.mail import EmailMessage
                    from django.conf import settings
                    from django.template.loader import render_to_string
                    
                    subject = "Welcome to Bio Med Ingredients Event Notifications!"
                    
                    html_message = render_to_string('main/email/general_email.html', {
                        'title': 'Subscription Confirmed',
                        'greeting': 'Hello,',
                        'intro_text': 'Thank you for subscribing to our event notifications!',
                        'outro_text': 'We will let you know whenever we post new exhibition events so you can stay up to date.'
                    })
                    
                    msg = EmailMessage(
                        subject,
                        html_message,
                        getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                        [email]
                    )
                    msg.content_subtype = "html"
                    msg.send(fail_silently=True)
                except Exception:
                    pass
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you! You will be notified of upcoming trade exhibitions.'
                })
            messages.success(request, 'Successfully subscribed to event notifications!')
        else:
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email address provided.'
                }, status=400)
            messages.error(request, 'Invalid email address provided.')
    if request.headers.get('referer'):
        return redirect(request.headers.get('referer'))
    return redirect('news_events')

# --- Dashboard: Exhibition Events ---
@login_required(login_url='dashboard_login')
def dashboard_manage_exhibition_events(request):
    synced_count = auto_sync_expired_exhibitions()
    if request.GET.get('sync') == '1':
        if synced_count > 0:
            messages.success(request, f'Event status check complete: {synced_count} past event(s) automatically marked as inactive.')
        else:
            messages.info(request, 'Event status check complete: all past events are already marked inactive.')
        return redirect('dashboard_manage_exhibition_events')
    events = ExhibitionEvent.objects.all().order_by('order', '-id')
    return render(request, 'main/dashboard/manage_exhibition_events.html', {'events': events})

@login_required(login_url='dashboard_login')
def dashboard_add_exhibition_event(request):
    if request.method == 'POST':
        form = ExhibitionEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Exhibition Event added successfully!')
            
            # Send automated newsletter to subscribers
            from .models import EventSubscriber
            from django.core.mail import EmailMessage
            from django.conf import settings
            from django.template.loader import render_to_string
            import threading
            
            subscribers = EventSubscriber.objects.filter(is_active=True)
            email_list = [sub.email for sub in subscribers]
            if email_list:
                html_message = render_to_string('main/email/newsletter_email.html', {
                    'subject': f"New Event Announced: {event.tag}",
                    'event': event,
                })
                
                def send_event_newsletter_async(subject, html_message, recipient_list):
                    msg = EmailMessage(
                        subject=subject,
                        body=html_message,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                        to=[],
                        bcc=recipient_list
                    )
                    msg.content_subtype = "html"
                    try:
                        msg.send(fail_silently=True)
                    except Exception:
                        pass
                
                thread = threading.Thread(target=send_event_newsletter_async, args=(f"New Event Announced: {event.tag}", html_message, email_list))
                thread.start()
                messages.success(request, f'Notification sent to {len(email_list)} subscribers.')

            return redirect('dashboard_manage_exhibition_events')
    else:
        form = ExhibitionEventForm()
    return render(request, 'main/dashboard/edit_exhibition_event.html', {'form': form, 'title': 'Add Exhibition Event'})

@login_required(login_url='dashboard_login')
def dashboard_edit_exhibition_event(request, pk):
    event = get_object_or_404(ExhibitionEvent, pk=pk)
    if request.method == 'POST':
        form = ExhibitionEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exhibition Event updated successfully!')
            return redirect('dashboard_manage_exhibition_events')
    else:
        form = ExhibitionEventForm(instance=event)
    return render(request, 'main/dashboard/edit_exhibition_event.html', {'form': form, 'title': 'Edit Exhibition Event', 'event': event})

@login_required(login_url='dashboard_login')
def dashboard_delete_exhibition_event(request, pk):
    event = get_object_or_404(ExhibitionEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Exhibition Event deleted successfully!')
        return redirect('dashboard_manage_exhibition_events')
    return render(request, 'main/dashboard/delete_exhibition_event.html', {'event': event})

# --- Dashboard: Instagram Posts ---
@login_required(login_url='dashboard_login')
def dashboard_manage_instagram_posts(request):
    posts = InstagramPost.objects.all().order_by('order', '-id')
    return render(request, 'main/dashboard/manage_instagram_posts.html', {'posts': posts})

@login_required(login_url='dashboard_login')
def dashboard_add_instagram_post(request):
    if request.method == 'POST':
        form = InstagramPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instagram Post added successfully!')
            return redirect('dashboard_manage_instagram_posts')
    else:
        form = InstagramPostForm()
    return render(request, 'main/dashboard/edit_instagram_post.html', {'form': form, 'title': 'Add Instagram Post'})

@login_required(login_url='dashboard_login')
def dashboard_edit_instagram_post(request, pk):
    post = get_object_or_404(InstagramPost, pk=pk)
    if request.method == 'POST':
        form = InstagramPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instagram Post updated successfully!')
            return redirect('dashboard_manage_instagram_posts')
    else:
        form = InstagramPostForm(instance=post)
    return render(request, 'main/dashboard/edit_instagram_post.html', {'form': form, 'title': 'Edit Instagram Post', 'post': post})

@login_required(login_url='dashboard_login')
def dashboard_delete_instagram_post(request, pk):
    post = get_object_or_404(InstagramPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Instagram Post deleted successfully!')
        return redirect('dashboard_manage_instagram_posts')
    return render(request, 'main/dashboard/delete_instagram_post.html', {'post': post})




# ==========================================
# Career / Job Frontend Views
# ==========================================

def career(request):
    jobs = JobOpening.objects.all()
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            job_id = request.POST.get('job_id')
            if job_id:
                application.job_id = job_id
                application.save()
                
                try:
                    from django.core.mail import send_mail
                    from django.conf import settings
                    email_config = EmailConfiguration.objects.first()
                    email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'
                    recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                    
                    from django.core.mail import EmailMessage
                    from django.template.loader import render_to_string
                    
                    subject = f"New Career Application from {application.name}"
                    
                    html_message = render_to_string('main/email/general_email.html', {
                        'title': 'New General Job Application',
                        'intro_text': 'A new career application has been submitted.',
                        'details': {
                            'Name': application.name,
                            'Email': application.email,
                            'Phone': application.phone,
                            'Job ID': job_id
                        },
                        'outro_text': 'Please check the admin dashboard to view the resume and complete details.'
                    })
                    
                    msg = EmailMessage(
                        subject,
                        html_message,
                        getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                        recipient_emails
                    )
                    msg.content_subtype = "html"
                    
                    if application.resume:
                        msg.attach_file(application.resume.path)
                        
                    msg.send(fail_silently=True)
                except Exception:
                    pass
                
                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('career')
    else:
        form = JobApplicationForm()
    return render(request, "main/career.html", {'jobs': jobs, 'form': form})

def job_detail(request, pk):
    from django.shortcuts import get_object_or_404
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            
            try:
                from django.core.mail import EmailMessage
                from django.conf import settings
                email_config = EmailConfiguration.objects.first()
                # Use dashboard config if available, fallback to design1@biomedingredients.com only if nothing exists
                email_str = email_config.career_email if email_config and email_config.career_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                subject = f"New Career Application from {application.name} for {job.title}"
                
                from django.template.loader import render_to_string
                html_message = render_to_string('main/email/general_email.html', {
                    'title': 'New Job Application',
                    'intro_text': f'A new career application has been submitted for {job.title} (ID: {job.id}).',
                    'details': {
                        'Name': application.name,
                        'Email': application.email,
                        'Phone': application.phone,
                        'Experience': f"{application.experience} Years",
                        'Address': application.address,
                        'Details': application.details
                    },
                    'outro_text': 'Please find the applicant\'s resume attached to this email. You can also view this application in the admin dashboard.'
                })
                
                email_msg = EmailMessage(
                    subject,
                    html_message,
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                    recipient_emails
                )
                email_msg.content_subtype = "html"
                
                if application.resume:
                    email_msg.attach_file(application.resume.path)
                    
                email_msg.send(fail_silently=True)
                
                # --- Send Auto-Reply to the Applicant ---
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                
                applicant_subject = f"Application Received: {job.title} - Bio Med Ingredients"
                html_message = render_to_string('main/email/application_received.html', {
                    'application': application,
                    'job': job
                })
                plain_message = strip_tags(html_message)
                
                applicant_email = EmailMessage(
                    applicant_subject,
                    html_message,
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                    [application.email]
                )
                applicant_email.content_subtype = "html" # Main content is text/html
                applicant_email.send(fail_silently=True)
                
            except Exception as e:
                print(f"Error sending email: {e}")
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=job.id)
    else:
        form = JobApplicationForm()
    
    return render(request, "main/job_detail.html", {'job': job, 'form': form})


# ==========================================
# Dashboard: Job Openings
# ==========================================

@login_required
def dashboard_manage_job_openings(request):
    jobs = JobOpening.objects.all().order_by('order')
    return render(request, 'main/dashboard/manage_job_openings.html', {'jobs': jobs, 'title': 'Manage Job Openings'})

@login_required
def dashboard_add_job_opening(request):
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Opening created successfully.')
            return redirect('dashboard_manage_job_openings')
    else:
        form = JobOpeningForm()
    return render(request, 'main/dashboard/edit_job_opening.html', {'form': form, 'title': 'Add Job Opening'})

@login_required
def dashboard_edit_job_opening(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        form = JobOpeningForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Opening updated successfully.')
            return redirect('dashboard_manage_job_openings')
    else:
        form = JobOpeningForm(instance=job)
    return render(request, 'main/dashboard/edit_job_opening.html', {'form': form, 'title': 'Edit Job Opening', 'job': job})

@login_required
def dashboard_delete_job_opening(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job Opening deleted successfully.')
        return redirect('dashboard_manage_job_openings')
    return render(request, 'main/dashboard/delete_job_opening.html', {'job': job})


# ==========================================
# Dashboard: Job Applications
# ==========================================

@login_required
def dashboard_manage_job_applications(request):
    applications = JobApplication.objects.select_related('job').all().order_by('-applied_at')
    return render(request, 'main/dashboard/manage_job_applications.html', {'applications': applications, 'title': 'Manage Job Applications'})

@login_required
def dashboard_view_job_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'main/dashboard/view_job_application.html', {'application': application, 'title': 'View Application'})

@login_required
def dashboard_delete_job_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Job Application deleted successfully.')
        return redirect('dashboard_manage_job_applications')
    return render(request, 'main/dashboard/delete_job_application.html', {'application': application})



# ==========================================
# Contact Us Views
# ==========================================

def contact_us(request):
    offices = OfficeLocation.objects.all().order_by('-is_hq', 'country')
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            
            try:
                from django.core.mail import EmailMessage
                from django.conf import settings
                from django.template.loader import render_to_string
                
                email_config = EmailConfiguration.objects.first()
                email_str = email_config.enquiry_email if email_config and email_config.enquiry_email else 'design1@biomedingredients.com'
                recipient_emails = [e.strip() for e in email_str.split(',') if e.strip()]
                
                subject = f"New Contact Message: {form.cleaned_data.get('subject')}"
                
                html_message = render_to_string('main/email/general_email.html', {
                    'title': 'New Contact Message',
                    'intro_text': 'A new contact message has been submitted from the website.',
                    'details': {
                        'Name': form.cleaned_data.get('name'),
                        'Email': form.cleaned_data.get('email'),
                        'Phone': form.cleaned_data.get('phone'),
                        'Country': form.cleaned_data.get('country'),
                        'Subject': form.cleaned_data.get('subject'),
                        'Message': form.cleaned_data.get('message')
                    }
                })
                
                msg = EmailMessage(
                    subject,
                    html_message,
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                    recipient_emails
                )
                msg.content_subtype = "html"
                msg.send(fail_silently=True)
            except Exception:
                pass
                
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactMessageForm()
        
    return render(request, "main/contact.html", {
        'form': form,
        'offices': offices
    })


# ==========================================
# Dashboard: Contact Messages
# ==========================================

@login_required
def dashboard_manage_contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'main/dashboard/manage_contact_messages.html', {'contact_messages': messages, 'title': 'Contact Messages'})

@login_required
def dashboard_view_contact_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'main/dashboard/view_contact_message.html', {'contact_message': msg, 'title': 'View Message'})

@login_required
def dashboard_delete_contact_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Contact message deleted successfully.')
        return redirect('dashboard_manage_contact_messages')
    return render(request, 'main/dashboard/delete_contact_message.html', {'contact_message': msg})

@login_required(login_url='dashboard_login')
def dashboard_email_configuration(request):
    config = EmailConfiguration.objects.first()
    if not config:
        config = EmailConfiguration()
    if request.method == 'POST':
        form = EmailConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email configuration updated successfully.')
            return redirect('dashboard_email_configuration')
    else:
        form = EmailConfigurationForm(instance=config)
    
    return render(request, 'main/dashboard/email_configuration_form.html', {
        'form': form
    })



# ==========================================
# Additional Product Category Views
# ==========================================

def nutritional_fine_chemicals(request):
    products = Product.objects.filter(category='nutritional_fine_chemicals').order_by('sub_category', 'name')
    return render(request, "main/nutritional-fine-chemicals.html", {"products": products})

def spices_and_oleoresins(request):
    products = Product.objects.filter(category='spices_and_oleoresins').order_by('sub_category', 'name')
    return render(request, "main/spices-and-oleoresins.html", {"products": products})

def raw_herbal_powders(request):
    products = Product.objects.filter(category='raw_herbal_powders').order_by('sub_category', 'name')
    return render(request, "main/raw-herbal-powders.html", {"products": products})

def organic_product_list(request):
    products = Product.objects.filter(category='organic_product_list').order_by('name')
    return render(request, "main/organic-product-list.html", {"products": products})


# --- Dashboard: Subscribers ---
@login_required(login_url='dashboard_login')
def dashboard_manage_subscribers(request):
    from .models import EventSubscriber
    subscribers = EventSubscriber.objects.all().order_by('-subscribed_at')
    return render(request, 'main/dashboard/manage_subscribers.html', {'subscribers': subscribers})

@login_required(login_url='dashboard_login')
def dashboard_delete_subscriber(request, pk):
    from .models import EventSubscriber
    if request.method == 'POST':
        subscriber = get_object_or_404(EventSubscriber, pk=pk)
        subscriber.delete()
        messages.success(request, 'Subscriber deleted successfully.')
    return redirect('dashboard_manage_subscribers')

@login_required(login_url='dashboard_login')
def dashboard_send_newsletter(request):
    from .models import EventSubscriber
    from django.core.mail import EmailMessage
    from django.conf import settings
    from django.template.loader import render_to_string
    import threading

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        
        if not subject or not message_body:
            messages.error(request, 'Subject and message are required.')
            return redirect('dashboard_manage_subscribers')
            
        subscribers = EventSubscriber.objects.filter(is_active=True)
        email_list = [sub.email for sub in subscribers]
        
        if not email_list:
            messages.warning(request, 'No active subscribers found.')
            return redirect('dashboard_manage_subscribers')

        html_message = render_to_string('main/email/newsletter_email.html', {
            'subject': subject,
            'message_body': message_body,
        })
        
        # Function to send emails in background so dashboard doesn't hang
        def send_newsletter_async(subject, html_message, recipient_list):
            msg = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                to=[], # Send as BCC so subscribers don't see each other
                bcc=recipient_list
            )
            msg.content_subtype = "html"
            try:
                msg.send(fail_silently=False)
            except Exception as e:
                print(f"Failed to send newsletter: {e}")

        # Start thread
        thread = threading.Thread(target=send_newsletter_async, args=(subject, html_message, email_list))
        thread.start()

        messages.success(request, f'Newsletter "{subject}" is being sent to {len(email_list)} subscribers.')
    return redirect('dashboard_manage_subscribers')


# ==========================================
# Legal & Compliance Views
# ==========================================
def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'main/terms_of_service.html')

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


# ==========================================
# Public Gallery View
# ==========================================
def gallery_page(request):
    images = GalleryImage.objects.all().order_by('order', '-created_at')
    return render(request, 'main/gallery.html', {'gallery_images': images})


# ==========================================
# Book Expo / Exhibition Meeting View
# ==========================================
def book_expo_meeting(request):
    import json
    from datetime import datetime, timedelta
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string

    auto_sync_expired_exhibitions()
    exhibitions = ExhibitionEvent.objects.filter(is_active=True).order_by('order', 'event_date')
    selected_expo_id = 0
    try:
        if request.GET.get('expo_id'):
            selected_expo_id = int(request.GET.get('expo_id'))
        elif exhibitions.exists():
            selected_expo_id = exhibitions.first().id
    except (ValueError, TypeError):
        selected_expo_id = exhibitions.first().id if exhibitions.exists() else 0

    # Build date range mapping per exhibition
    expo_dates_map = {}
    for ex in exhibitions:
        dates = []
        if ex.event_date:
            cur = ex.event_date
            end = ex.event_end_date or ex.event_date
            while cur <= end:
                dates.append({
                    'value': cur.strftime('%Y-%m-%d'),
                    'text': cur.strftime('%a, %b %d, %Y')
                })
                cur += timedelta(days=1)
        expo_dates_map[str(ex.id)] = dates

    # Build booked times mapping
    booked_times_map = {}
    active_bookings = ExpoMeetingBooking.objects.filter(status__in=['pending', 'accepted'])
    for b in active_bookings:
        eid = str(b.expo_id)
        dstr = b.meeting_date.strftime('%Y-%m-%d')
        tstr = b.meeting_time.strftime('%H:%M')
        if eid not in booked_times_map:
            booked_times_map[eid] = {}
        if dstr not in booked_times_map[eid]:
            booked_times_map[eid][dstr] = []
        booked_times_map[eid][dstr].append(tstr)

    booking_success = False
    created_booking = None

    if request.method == 'POST':
        # Honeypot check
        if request.POST.get('b_website_url'):
            booking_success = True
            messages.success(request, 'Your meeting request has been submitted successfully!')
            return render(request, 'main/book_expo_meeting.html', {
                'exhibitions': exhibitions,
                'selected_expo_id': selected_expo_id,
                'expo_dates_json': json.dumps(expo_dates_map),
                'booked_times_json': json.dumps(booked_times_map),
                'booking_success': True,
            })

        expo_id = request.POST.get('expo')
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        company = request.POST.get('company', '').strip()
        phone = request.POST.get('phone', '').strip()
        meeting_date = request.POST.get('meeting_date', '').strip()
        meeting_time = request.POST.get('meeting_time', '').strip()
        message_txt = request.POST.get('message', '').strip()

        if not expo_id or not name or not email or not phone or not meeting_date or not meeting_time:
            messages.error(request, 'Please complete all required fields.')
        else:
            expo_obj = get_object_or_404(ExhibitionEvent, pk=expo_id)
            try:
                m_date = datetime.strptime(meeting_date, '%Y-%m-%d').date()
                m_time = datetime.strptime(meeting_time, '%H:%M').time()

                # Check double booking
                conflict = ExpoMeetingBooking.objects.filter(
                    expo=expo_obj,
                    meeting_date=m_date,
                    meeting_time=m_time,
                    status__in=['pending', 'accepted']
                ).exists()

                if conflict:
                    messages.error(request, 'This time slot was just reserved. Please select another time.')
                else:
                    created_booking = ExpoMeetingBooking.objects.create(
                        expo=expo_obj,
                        name=name,
                        email=email,
                        company=company,
                        phone=phone,
                        meeting_date=m_date,
                        meeting_time=m_time,
                        message=message_txt,
                        status='pending'
                    )
                    booking_success = True
                    messages.success(request, 'Your meeting request has been submitted successfully! We will confirm shortly.')

                    # Send Email Notification
                    try:
                        email_config = EmailConfiguration.objects.first()
                        target_email_str = email_config.booking_email if email_config and email_config.booking_email else 'design1@biomedingredients.com'
                        recipients = [e.strip() for e in target_email_str.split(',') if e.strip()]

                        subject = f"New Expo Meeting Booking: {name} at {expo_obj.tag}"
                        html_content = render_to_string('main/email/general_email.html', {
                            'title': 'New Trade Expo Meeting Scheduled',
                            'intro_text': f"A new client consultation has been booked for {expo_obj.tag}.",
                            'details': {
                                'Exhibition': expo_obj.tag,
                                'Booth': expo_obj.booth_number or 'N/A',
                                'Meeting Date': m_date.strftime('%B %d, %Y'),
                                'Meeting Time': m_time.strftime('%I:%M %p'),
                                'Delegate Name': name,
                                'Company': company or 'N/A',
                                'Email': email,
                                'Phone / WhatsApp': phone,
                                'Agenda': message_txt or 'N/A'
                            }
                        })
                        msg = EmailMessage(
                            subject,
                            html_content,
                            getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@biomedingredients.com'),
                            recipients
                        )
                        msg.content_subtype = "html"
                        msg.send(fail_silently=True)
                    except Exception as err:
                        print(f"Failed to send booking notification email: {err}")

            except ValueError:
                messages.error(request, 'Invalid date or time format.')

    return render(request, 'main/book_expo_meeting.html', {
        'exhibitions': exhibitions,
        'selected_expo_id': selected_expo_id,
        'expo_dates_json': json.dumps(expo_dates_map),
        'booked_times_json': json.dumps(booked_times_map),
        'booking_success': booking_success,
        'booking': created_booking
    })


# ==========================================
# Dashboard: Expo Meeting Bookings
# ==========================================
@login_required(login_url='dashboard_login')
def dashboard_manage_expo_bookings(request):
    bookings = ExpoMeetingBooking.objects.all().order_by('-created_at')
    return render(request, 'main/dashboard/manage_expo_bookings.html', {'bookings': bookings})

@login_required(login_url='dashboard_login')
def dashboard_expo_booking_status(request, pk):
    booking = get_object_or_404(ExpoMeetingBooking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'accepted', 'rejected']:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking status updated to {new_status}.')
    return redirect('dashboard_manage_expo_bookings')

@login_required(login_url='dashboard_login')
def dashboard_delete_expo_booking(request, pk):
    booking = get_object_or_404(ExpoMeetingBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Expo meeting booking deleted.')
    return redirect('dashboard_manage_expo_bookings')


# ==========================================
# Dashboard: Unified B2B Leads Manager
# ==========================================
@login_required(login_url='dashboard_login')
def dashboard_manage_leads(request):
    from django.urls import reverse

    lead_type = request.GET.get('type', '').strip()
    search_q = request.GET.get('q', '').strip().lower()

    leads = []

    # 1. Product Enquiries
    if not lead_type or lead_type == 'enquiry':
        enquiries = Enquiry.objects.all().order_by('-created_at')
        for e in enquiries:
            if search_q and search_q not in (e.full_name + ' ' + (e.company or '') + ' ' + e.email + ' ' + e.product_name).lower():
                continue
            leads.append({
                'id': e.id,
                'type': 'enquiry',
                'date': e.created_at,
                'name': e.full_name,
                'company': e.company,
                'country': '',
                'email': e.email,
                'phone': '',
                'subject': e.product_name,
                'meta_info': 'Product Spec Inquiry',
                'message': e.message,
                'detail_url': reverse('manage_enquiries'),
                'resume_url': ''
            })

    # 2. Contact Messages
    if not lead_type or lead_type == 'contact':
        contacts = ContactMessage.objects.all().order_by('-created_at')
        for c in contacts:
            if search_q and search_q not in (c.name + ' ' + c.email + ' ' + c.country + ' ' + c.subject).lower():
                continue
            leads.append({
                'id': c.id,
                'type': 'contact',
                'date': c.created_at,
                'name': c.name,
                'company': '',
                'country': c.country,
                'email': c.email,
                'phone': c.phone,
                'subject': c.subject,
                'meta_info': 'General Contact Desk',
                'message': c.message,
                'detail_url': reverse('dashboard_view_contact_message', args=[c.id]),
                'resume_url': ''
            })

    # 3. Expo Meeting Bookings
    if not lead_type or lead_type == 'expo':
        expo_bookings = ExpoMeetingBooking.objects.all().order_by('-created_at')
        for b in expo_bookings:
            if search_q and search_q not in (b.name + ' ' + (b.company or '') + ' ' + b.email + ' ' + b.expo.tag).lower():
                continue
            leads.append({
                'id': b.id,
                'type': 'expo',
                'date': b.created_at,
                'name': b.name,
                'company': b.company,
                'country': '',
                'email': b.email,
                'phone': b.phone,
                'subject': f"{b.expo.tag} ({b.meeting_date.strftime('%b %d')} @ {b.meeting_time.strftime('%I:%M %p')})",
                'meta_info': f"Status: {b.status.capitalize()}",
                'message': b.message,
                'detail_url': reverse('dashboard_manage_expo_bookings'),
                'resume_url': ''
            })

    # 4. Job Applications
    if not lead_type or lead_type == 'career':
        apps = JobApplication.objects.all().order_by('-applied_at')
        for a in apps:
            pos_title = a.job.title if a.job else 'General Application'
            if search_q and search_q not in (a.name + ' ' + a.email + ' ' + pos_title).lower():
                continue
            leads.append({
                'id': a.id,
                'type': 'career',
                'date': a.applied_at,
                'name': a.name,
                'company': 'Candidate Applicant',
                'country': '',
                'email': a.email,
                'phone': a.phone,
                'subject': pos_title,
                'meta_info': 'Career Applicant',
                'message': f"Experience: {a.experience} years. {a.details or ''}",
                'detail_url': reverse('dashboard_view_job_application', args=[a.id]),
                'resume_url': a.resume.url if a.resume else ''
            })

    # Sort unified leads by descending date
    leads.sort(key=lambda x: x['date'], reverse=True)

    return render(request, 'main/dashboard/manage_leads.html', {
        'leads': leads,
        'current_type': lead_type,
        'search_query': search_q,
        'total_enquiries_count': Enquiry.objects.count(),
        'total_contacts_count': ContactMessage.objects.count(),
        'total_expo_count': ExpoMeetingBooking.objects.count(),
        'total_applications_count': JobApplication.objects.count(),
    })

@login_required(login_url='dashboard_login')
def dashboard_export_leads_csv(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="biomed_leads_export.csv"'
    # Write Excel UTF-8 BOM
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['Lead ID', 'Type', 'Date', 'Full Name', 'Company', 'Country', 'Email', 'Phone', 'Subject / Target', 'Message / Notes'])

    lead_type = request.GET.get('type', '').strip()
    search_q = request.GET.get('q', '').strip().lower()

    if not lead_type or lead_type == 'enquiry':
        for e in Enquiry.objects.all().order_by('-created_at'):
            if not search_q or search_q in (e.full_name + ' ' + (e.company or '') + ' ' + e.email + ' ' + e.product_name).lower():
                writer.writerow([e.id, 'Product Enquiry', e.created_at.strftime('%Y-%m-%d %H:%M'), e.full_name, e.company or '', '', e.email, '', e.product_name, e.message])

    if not lead_type or lead_type == 'contact':
        for c in ContactMessage.objects.all().order_by('-created_at'):
            if not search_q or search_q in (c.name + ' ' + c.email + ' ' + c.country + ' ' + c.subject).lower():
                writer.writerow([c.id, 'Contact Message', c.created_at.strftime('%Y-%m-%d %H:%M'), c.name, '', c.country, c.email, c.phone, c.subject, c.message])

    if not lead_type or lead_type == 'expo':
        for b in ExpoMeetingBooking.objects.all().order_by('-created_at'):
            if not search_q or search_q in (b.name + ' ' + (b.company or '') + ' ' + b.email + ' ' + b.expo.tag).lower():
                writer.writerow([b.id, 'Expo Meeting', b.created_at.strftime('%Y-%m-%d %H:%M'), b.name, b.company or '', '', b.email, b.phone, f"{b.expo.tag} ({b.meeting_date} {b.meeting_time})", b.message or ''])

    if not lead_type or lead_type == 'career':
        for a in JobApplication.objects.all().order_by('-applied_at'):
            pos = a.job.title if a.job else 'General Application'
            if not search_q or search_q in (a.name + ' ' + a.email + ' ' + pos).lower():
                writer.writerow([a.id, 'Career Applicant', a.applied_at.strftime('%Y-%m-%d %H:%M'), a.name, 'Candidate', '', a.email, a.phone, pos, a.details or ''])

    return response


# ==========================================
# Dashboard: Analytics Overview
# ==========================================
@login_required(login_url='dashboard_login')
def dashboard_analytics(request):
    enquiries_count = Enquiry.objects.count()
    contacts_count = ContactMessage.objects.count()
    expo_count = ExpoMeetingBooking.objects.count()
    apps_count = JobApplication.objects.count()
    subs_count = EventSubscriber.objects.count()

    recent_items = []
    for e in Enquiry.objects.all().order_by('-created_at')[:4]:
        recent_items.append({'type_label': 'Inquiry', 'name': e.full_name, 'sub_text': e.product_name, 'time': e.created_at})
    for b in ExpoMeetingBooking.objects.all().order_by('-created_at')[:4]:
        recent_items.append({'type_label': 'Expo Booking', 'name': b.name, 'sub_text': b.expo.tag, 'time': b.created_at})
    for c in ContactMessage.objects.all().order_by('-created_at')[:4]:
        recent_items.append({'type_label': 'Contact Msg', 'name': c.name, 'sub_text': c.subject, 'time': c.created_at})

    recent_items.sort(key=lambda x: x['time'], reverse=True)

    return render(request, 'main/dashboard/analytics.html', {
        'total_enquiries': enquiries_count,
        'total_contacts': contacts_count,
        'total_expo': expo_count,
        'total_applications': apps_count,
        'total_subscribers': subs_count,
        'recent_items': recent_items[:8]
    })


# ==========================================
# Dashboard: Image Compressor Tool
# ==========================================
@login_required(login_url='dashboard_login')
def dashboard_compressor(request):
    import os
    from django.conf import settings
    from PIL import Image

    scan_dirs = [
        os.path.join(settings.BASE_DIR, 'media'),
        os.path.join(settings.BASE_DIR, 'static', 'images')
    ]

    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    items = []
    total_count = 0
    total_size = 0
    compressible_count = 0
    est_savings = 0

    for base in scan_dirs:
        if not os.path.exists(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in valid_exts:
                    full_p = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(full_p)
                        total_count += 1
                        total_size += sz

                        rel_p = os.path.relpath(full_p, settings.BASE_DIR).replace('\\', '/')

                        with Image.open(full_p) as im:
                            w, h = im.size

                        is_compressible = (max(w, h) > 1920) or (sz > 200 * 1024)
                        if is_compressible:
                            compressible_count += 1
                            est_saved = int(sz * 0.5)
                            est_savings += est_saved
                        else:
                            est_saved = 0

                        items.append({
                            'path': rel_p,
                            'width': w,
                            'height': h,
                            'size_kb': round(sz / 1024, 1),
                            'is_compressible': is_compressible,
                            'est_saved_kb': round(est_saved / 1024, 1)
                        })
                    except Exception:
                        pass

    # Sort by size descending
    items.sort(key=lambda x: x['size_kb'], reverse=True)

    return render(request, 'main/dashboard/compressor.html', {
        'items': items[:100],
        'total_images': total_count,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'compressible_count': compressible_count,
        'est_savings_mb': round(est_savings / (1024 * 1024), 2)
    })

@login_required(login_url='dashboard_login')
def dashboard_compressor_save(request):
    from django.http import JsonResponse
    import os
    from django.conf import settings

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})

    rel_path = request.POST.get('path', '').replace('\\', '/').strip('/')
    uploaded_file = request.FILES.get('file')

    if not rel_path or not uploaded_file:
        return JsonResponse({'success': False, 'error': 'Missing parameters'})

    if not (rel_path.startswith('media/') or rel_path.startswith('static/images/')):
        return JsonResponse({'success': False, 'error': 'Unauthorized directory'})

    full_dest = os.path.join(settings.BASE_DIR, rel_path.replace('/', os.sep))
    if not os.path.exists(full_dest):
        return JsonResponse({'success': False, 'error': 'File not found on disk'})

    try:
        with open(full_dest, 'wb') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        return JsonResponse({'success': True, 'path': rel_path})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ==========================================
# Dashboard: PDF Thumbnails Tool
# ==========================================
@login_required(login_url='dashboard_login')
def dashboard_pdf_thumbnails(request):
    import os
    from django.conf import settings

    scan_targets = [
        {
            'collection': 'Product Documents',
            'pdf_dir': os.path.join(settings.BASE_DIR, 'media', 'product_documents'),
            'thumb_dir': os.path.join(settings.BASE_DIR, 'media', 'product_documents', 'thumbnails'),
            'pdf_rel': 'media/product_documents/',
            'thumb_rel': 'media/product_documents/thumbnails/'
        },
        {
            'collection': 'Product Brochures',
            'pdf_dir': os.path.join(settings.BASE_DIR, 'media', 'brochures', 'pdfs'),
            'thumb_dir': os.path.join(settings.BASE_DIR, 'media', 'brochures', 'thumbnails'),
            'pdf_rel': 'media/brochures/pdfs/',
            'thumb_rel': 'media/brochures/thumbnails/'
        }
    ]

    items = []
    total_pdfs = 0
    ready_count = 0
    missing_count = 0

    for target in scan_targets:
        p_dir = target['pdf_dir']
        t_dir = target['thumb_dir']
        if not os.path.exists(p_dir):
            continue
        if not os.path.exists(t_dir):
            os.makedirs(t_dir, exist_ok=True)

        for f in os.listdir(p_dir):
            if f.lower().endswith('.pdf'):
                total_pdfs += 1
                base_name = os.path.splitext(f)[0]
                expected_thumb = os.path.join(t_dir, base_name + '.webp')
                has_thumb = os.path.exists(expected_thumb)
                if has_thumb:
                    ready_count += 1
                else:
                    missing_count += 1

                pdf_sz = os.path.getsize(os.path.join(p_dir, f))
                items.append({
                    'name': base_name.replace('_', ' ').replace('-', ' ').title(),
                    'filename': f,
                    'collection': target['collection'],
                    'rel_pdf_path': target['pdf_rel'] + f,
                    'rel_thumb_path': target['thumb_rel'] + base_name + '.webp',
                    'has_thumb': has_thumb,
                    'pdf_size_kb': round(pdf_sz / 1024, 1)
                })

    items.sort(key=lambda x: (x['has_thumb'], x['name']))

    return render(request, 'main/dashboard/pdf_thumbnails.html', {
        'items': items,
        'total_pdfs': total_pdfs,
        'ready_count': ready_count,
        'missing_count': missing_count
    })

@login_required(login_url='dashboard_login')
def dashboard_pdf_thumbnail_save(request):
    from django.http import JsonResponse
    import os
    from django.conf import settings

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})

    thumb_rel = request.POST.get('thumb_path', '').replace('\\', '/').strip('/')
    uploaded_file = request.FILES.get('file')

    if not thumb_rel or not uploaded_file:
        return JsonResponse({'success': False, 'error': 'Missing parameters'})

    if not (thumb_rel.startswith('media/product_documents/thumbnails/') or thumb_rel.startswith('media/brochures/thumbnails/')):
        return JsonResponse({'success': False, 'error': 'Unauthorized directory'})

    full_dest = os.path.join(settings.BASE_DIR, thumb_rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_dest), exist_ok=True)

    try:
        with open(full_dest, 'wb') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        return JsonResponse({'success': True, 'path': thumb_rel})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ==========================================
# Dynamic XML Sitemap Generator
# ==========================================
def sitemap_xml(request):
    from django.http import HttpResponse
    from datetime import date
    from django.urls import reverse

    base_url = request.build_absolute_uri('/')[:-1]
    today = date.today().strftime('%Y-%m-%d')

    core_routes = [
        ('', '1.0', 'daily'),
        (reverse('about'), '0.8', 'monthly'),
        (reverse('team'), '0.7', 'monthly'),
        (reverse('infrastructure'), '0.8', 'monthly'),
        (reverse('facility'), '0.8', 'monthly'),
        (reverse('research'), '0.8', 'monthly'),
        (reverse('accreditations'), '0.8', 'monthly'),
        (reverse('product_range'), '0.9', 'weekly'),
        (reverse('herbal_extracts'), '0.9', 'weekly'),
        (reverse('natural_food_colors'), '0.9', 'weekly'),
        (reverse('nutritional_fine_chemicals'), '0.9', 'weekly'),
        (reverse('spices_and_oleoresins'), '0.9', 'weekly'),
        (reverse('raw_herbal_powders'), '0.9', 'weekly'),
        (reverse('organic_product_list'), '0.8', 'weekly'),
        (reverse('product_brochures'), '0.8', 'monthly'),
        (reverse('product_documents'), '0.8', 'monthly'),
        (reverse('gallery'), '0.7', 'weekly'),
        (reverse('news_events'), '0.8', 'weekly'),
        (reverse('book_expo_meeting'), '0.9', 'weekly'),
        (reverse('career'), '0.7', 'monthly'),
        (reverse('csr'), '0.7', 'monthly'),
        (reverse('contact'), '0.8', 'monthly'),
        (reverse('privacy_policy'), '0.5', 'yearly'),
        (reverse('terms_of_service'), '0.5', 'yearly'),
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority, freq in core_routes:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{path}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append(f'    <changefreq>{freq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')

    # Dynamic Brands
    for b in Brand.objects.all():
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{reverse("brand_detail", args=[b.id])}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>0.85</priority>')
        xml.append('  </url>')

    # Dynamic Research Areas
    for r in ResearchArea.objects.all():
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{reverse("research_area_detail", args=[r.slug])}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append('    <priority>0.8</priority>')
        xml.append('  </url>')

    xml.append('</urlset>')

    return HttpResponse('\n'.join(xml), content_type='application/xml')


@login_required(login_url='dashboard_login')
def dashboard_sitemap(request):
    from django.urls import reverse

    base_url = request.build_absolute_uri('/')[:-1]

    url_items = [
        {'title': 'Home', 'category': 'Core Page', 'loc': base_url + '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'title': 'About Company', 'category': 'Corporate', 'loc': base_url + reverse('about'), 'priority': '0.8', 'changefreq': 'monthly'},
        {'title': 'Management Team', 'category': 'Corporate', 'loc': base_url + reverse('team'), 'priority': '0.7', 'changefreq': 'monthly'},
        {'title': 'Herbal Extracts', 'category': 'Product Catalog', 'loc': base_url + reverse('herbal_extracts'), 'priority': '0.9', 'changefreq': 'weekly'},
        {'title': 'Natural Food Colors & Flavours', 'category': 'Product Catalog', 'loc': base_url + reverse('natural_food_colors'), 'priority': '0.9', 'changefreq': 'weekly'},
        {'title': 'Product Documents & COAs', 'category': 'Technical', 'loc': base_url + reverse('product_documents'), 'priority': '0.8', 'changefreq': 'monthly'},
        {'title': 'Public Gallery', 'category': 'Showcase', 'loc': base_url + reverse('gallery'), 'priority': '0.7', 'changefreq': 'weekly'},
        {'title': 'Book an Expo Meeting', 'category': 'Trade Shows', 'loc': base_url + reverse('book_expo_meeting'), 'priority': '0.9', 'changefreq': 'weekly'},
        {'title': 'News & Exhibitions', 'category': 'Events', 'loc': base_url + reverse('news_events'), 'priority': '0.8', 'changefreq': 'weekly'},
        {'title': 'Contact Us', 'category': 'Contact', 'loc': base_url + reverse('contact'), 'priority': '0.8', 'changefreq': 'monthly'},
        {'title': 'Privacy Statement', 'category': 'Compliance', 'loc': base_url + reverse('privacy_policy'), 'priority': '0.5', 'changefreq': 'yearly'},
        {'title': 'Terms of Service', 'category': 'Compliance', 'loc': base_url + reverse('terms_of_service'), 'priority': '0.5', 'changefreq': 'yearly'},
    ]

    for b in Brand.objects.all():
        url_items.append({
            'title': f'Brand: {b.name}',
            'category': 'Brand',
            'loc': base_url + reverse('brand_detail', args=[b.id]),
            'priority': '0.85',
            'changefreq': 'weekly'
        })

    return render(request, 'main/dashboard/sitemap.html', {
        'url_items': url_items,
        'total_urls': len(url_items),
        'static_count': 12,
        'dynamic_count': max(0, len(url_items) - 12)
    })

