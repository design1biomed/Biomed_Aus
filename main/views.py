from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import IndexPageContent, Accreditation, QualityTimeline, ExtractCategory, CorePromise, OfficeLocation, Enquiry, SolutionFeature, AboutPageContent
from .forms import IndexPageForm, AccreditationForm, QualityTimelineForm, ExtractCategoryForm, CorePromiseForm, OfficeLocationForm, SolutionFeatureForm, AboutPageForm

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
        'features': features
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
        
        messages.success(request, 'Thank you! Your enquiry has been submitted. Our team will contact you shortly.')
        return redirect('index')
    
    return redirect('index')

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
