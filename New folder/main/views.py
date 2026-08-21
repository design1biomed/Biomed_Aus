from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import IndexPageContent, Accreditation, QualityTimeline, ExtractCategory, CorePromise, OfficeLocation, Enquiry, SolutionFeature, AboutPageContent, CSRPageContent, TeamMember, OperationTeamMember, InfrastructurePageContent, ResearchArea, ResearchCoreAreaLink, GalleryImage, Brand, ProductRangeSlide, Product, NaturalFoodColor, NaturalFlavour, ProductBrochure, ProductDocumentCategory, ProductDocument, ExhibitionEvent, EventSubscriber, InstagramPost, JobOpening, JobApplication, ContactMessage, EmailConfiguration
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
    return render(request, 'main/dashboard/dashboard.html')

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

# --- News & Events Front-end View ---
def news_events(request):
    instagram_posts = InstagramPost.objects.filter(is_visible=True)
    exhibitions = ExhibitionEvent.objects.filter(is_active=True).order_by('order', '-id')
    return render(request, "main/news_events.html", {
        "instagram_posts": instagram_posts,
        "exhibitions": exhibitions
    })

def subscribe_event_notifications(request):
    if request.method == "POST":
        email = request.POST.get("email")
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
            messages.success(request, 'Successfully subscribed to event notifications!')
        else:
            messages.error(request, 'Invalid email address provided.')
    return redirect('news_events')

# --- Dashboard: Exhibition Events ---
@login_required(login_url='dashboard_login')
def dashboard_manage_exhibition_events(request):
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
