from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('dashboard/', views.custom_dashboard, name='custom_dashboard'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/edit-index/', views.edit_index_page, name='edit_index_page'),
    path('dashboard/about/', views.edit_about_page, name='edit_about_page'),
    path('dashboard/accreditations/', views.manage_accreditations, name='manage_accreditations'),
    path('dashboard/accreditations/add/', views.add_accreditation, name='add_accreditation'),
    path('dashboard/accreditations/edit/<int:pk>/', views.edit_accreditation, name='edit_accreditation'),
    path('dashboard/accreditations/delete/<int:pk>/', views.delete_accreditation, name='delete_accreditation'),
    
    path('dashboard/timelines/', views.manage_timelines, name='manage_timelines'),
    path('dashboard/timelines/add/', views.add_timeline, name='add_timeline'),
    path('dashboard/timelines/edit/<int:pk>/', views.edit_timeline, name='edit_timeline'),
    path('dashboard/timelines/delete/<int:pk>/', views.delete_timeline, name='delete_timeline'),
    
    path('dashboard/extracts/', views.manage_extracts, name='manage_extracts'),
    path('dashboard/extracts/add/', views.add_extract, name='add_extract'),
    path('dashboard/extracts/edit/<int:pk>/', views.edit_extract, name='edit_extract'),
    path('dashboard/extracts/delete/<int:pk>/', views.delete_extract, name='delete_extract'),
    
    path('dashboard/promises/', views.manage_promises, name='manage_promises'),
    path('dashboard/promises/add/', views.add_promise, name='add_promise'),
    path('dashboard/promises/edit/<int:pk>/', views.edit_promise, name='edit_promise'),
    path('dashboard/promises/delete/<int:pk>/', views.delete_promise, name='delete_promise'),
    
    path('dashboard/offices/', views.manage_offices, name='manage_offices'),
    path('dashboard/offices/add/', views.add_office, name='add_office'),
    path('dashboard/offices/edit/<int:pk>/', views.edit_office, name='edit_office'),
    path('dashboard/offices/delete/<int:pk>/', views.delete_office, name='delete_office'),
    
    path('dashboard/solutions/', views.manage_solutions, name='manage_solutions'),
    path('dashboard/solutions/add/', views.add_solution, name='add_solution'),
    path('dashboard/solutions/edit/<int:pk>/', views.edit_solution, name='edit_solution'),
    path('dashboard/solutions/delete/<int:pk>/', views.delete_solution, name='delete_solution'),
    
    path('dashboard/enquiries/', views.manage_enquiries, name='manage_enquiries'),
    path('dashboard/enquiries/delete/<int:pk>/', views.delete_enquiry, name='delete_enquiry'),
]
