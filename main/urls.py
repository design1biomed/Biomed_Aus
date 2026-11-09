from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about'),
    path('csr/', views.csr_page, name='csr'),
    path('infrastructure-and-services/', views.infrastructure_page, name='infrastructure'),
    path('facility/', views.facility_page, name='facility'),
    path('research/', views.research_page, name='research'),
    path('research/<slug:slug>/', views.research_area_detail, name='research_area_detail'),
    path('accreditations/', views.accreditations_page, name='accreditations'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('dashboard/', views.custom_dashboard, name='custom_dashboard'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/edit-index/', views.edit_index_page, name='edit_index_page'),
    path('dashboard/about/', views.edit_about_page, name='edit_about_page'),
    path('dashboard/csr/', views.edit_csr_page, name='edit_csr_page'),
    path('dashboard/infrastructure/', views.edit_infrastructure_page, name='edit_infrastructure_page'),
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
    
    path('team/', views.team_page, name='team'),
    path('dashboard/team/', views.manage_team, name='manage_team'),
    path('dashboard/team/add/<str:team_type>/', views.add_team_member, name='add_team_member'),
    path('dashboard/team/edit/<str:team_type>/<int:pk>/', views.edit_team_member, name='edit_team_member'),
    path('dashboard/team/delete/<str:team_type>/<int:pk>/', views.delete_team_member, name='delete_team_member'),
    
    path('dashboard/research/', views.manage_research, name='manage_research'),
    path('dashboard/research/add/', views.add_research_area, name='add_research_area'),
    path('dashboard/research/edit/<int:pk>/', views.edit_research_area, name='edit_research_area'),
    path('dashboard/research/delete/<int:pk>/', views.delete_research_area, name='delete_research_area'),
    
    path('dashboard/research/core-link/add/', views.add_core_link, name='add_core_link'),
    path('dashboard/research/core-link/edit/<int:pk>/', views.edit_core_link, name='edit_core_link'),
    path('dashboard/research/core-link/delete/<int:pk>/', views.delete_core_link, name='delete_core_link'),
    
    path('dashboard/research/gallery/add/', views.add_gallery_image, name='add_gallery_image'),
    path('dashboard/research/gallery/edit/<int:pk>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('dashboard/research/gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    
    # Brands / Trademarks
    path('brands/', views.brands_list, name='brands_list'),
    path('brands/<int:pk>/', views.brand_detail, name='brand_detail'),
    path('dashboard/brands/', views.dashboard_manage_brands, name='dashboard_manage_brands'),
    path('dashboard/brands/add/', views.dashboard_add_brand, name='dashboard_add_brand'),
    path('dashboard/brands/edit/<int:pk>/', views.dashboard_edit_brand, name='dashboard_edit_brand'),
    path('dashboard/brands/delete/<int:pk>/', views.dashboard_delete_brand, name='dashboard_delete_brand'),

    # Product Range
    path('product-range/', views.product_range, name='product_range'),
    path('dashboard/product-range/', views.dashboard_manage_product_range, name='dashboard_manage_product_range'),
    path('dashboard/product-range/add/', views.dashboard_add_product_range, name='dashboard_add_product_range'),
    path('dashboard/product-range/edit/<int:pk>/', views.dashboard_edit_product_range, name='dashboard_edit_product_range'),
    path('dashboard/product-range/delete/<int:pk>/', views.dashboard_delete_product_range, name='dashboard_delete_product_range'),

    # Herbal Extracts (Products)
    path('herbal-extracts/', views.herbal_extracts, name='herbal_extracts'),
    path('dashboard/products/', views.dashboard_manage_products, name='dashboard_manage_products'),
    path('dashboard/products/add/', views.dashboard_add_product, name='dashboard_add_product'),
    path('dashboard/products/edit/<int:pk>/', views.dashboard_edit_product, name='dashboard_edit_product'),
    path('dashboard/products/delete/<int:pk>/', views.dashboard_delete_product, name='dashboard_delete_product'),

    # Natural Food Colors and Flavours
    path('natural-food-colors/', views.natural_food_colors, name='natural_food_colors'),
    
    path('nutritional-fine-chemicals/', views.nutritional_fine_chemicals, name='nutritional_fine_chemicals'),
    path('organic-product-list/', views.organic_product_list, name='organic_product_list'),
    path('spices-and-oleoresins/', views.spices_and_oleoresins, name='spices_and_oleoresins'),
    path('raw-herbal-powders/', views.raw_herbal_powders, name='raw_herbal_powders'),
    path('dashboard/natural-food-colors/', views.dashboard_manage_natural_food_colors, name='dashboard_manage_natural_food_colors'),
    path('dashboard/natural-food-colors/add/', views.dashboard_add_natural_food_color, name='dashboard_add_natural_food_color'),
    path('dashboard/natural-food-colors/edit/<int:pk>/', views.dashboard_edit_natural_food_color, name='dashboard_edit_natural_food_color'),
    path('dashboard/natural-food-colors/delete/<int:pk>/', views.dashboard_delete_natural_food_color, name='dashboard_delete_natural_food_color'),
    path('dashboard/natural-flavours/', views.dashboard_manage_natural_flavours, name='dashboard_manage_natural_flavours'),
    path('dashboard/natural-flavours/add/', views.dashboard_add_natural_flavour, name='dashboard_add_natural_flavour'),
    path('dashboard/natural-flavours/edit/<int:pk>/', views.dashboard_edit_natural_flavour, name='dashboard_edit_natural_flavour'),
    path('dashboard/natural-flavours/delete/<int:pk>/', views.dashboard_delete_natural_flavour, name='dashboard_delete_natural_flavour'),

    # Product Brochures
    path('product-brochures/', views.product_brochures, name='product_brochures'),
    path('dashboard/product-brochures/', views.dashboard_manage_product_brochures, name='dashboard_manage_product_brochures'),
    path('dashboard/product-brochures/add/', views.dashboard_add_product_brochure, name='dashboard_add_product_brochure'),
    path('dashboard/product-brochures/edit/<int:pk>/', views.dashboard_edit_product_brochure, name='dashboard_edit_product_brochure'),
    path('dashboard/product-brochures/delete/<int:pk>/', views.dashboard_delete_product_brochure, name='dashboard_delete_product_brochure'),

    # Product Documents
    path('product-documents/', views.product_documents, name='product_documents'),
    path('dashboard/product-document-categories/', views.dashboard_manage_product_document_categories, name='dashboard_manage_product_document_categories'),
    path('dashboard/product-document-categories/add/', views.dashboard_add_product_document_category, name='dashboard_add_product_document_category'),
    path('dashboard/product-document-categories/edit/<int:pk>/', views.dashboard_edit_product_document_category, name='dashboard_edit_product_document_category'),
    path('dashboard/product-document-categories/delete/<int:pk>/', views.dashboard_delete_product_document_category, name='dashboard_delete_product_document_category'),
    path('dashboard/product-documents/', views.dashboard_manage_product_documents, name='dashboard_manage_product_documents'),
    path('dashboard/product-documents/add/', views.dashboard_add_product_document, name='dashboard_add_product_document'),
    path('dashboard/product-documents/edit/<int:pk>/', views.dashboard_edit_product_document, name='dashboard_edit_product_document'),
    path('dashboard/product-documents/delete/<int:pk>/', views.dashboard_delete_product_document, name='dashboard_delete_product_document'),

    # News & Events
    path('news-events/', views.news_events, name='news_events'),
    path('subscribe-events/', views.subscribe_event_notifications, name='subscribe_event_notifications'),

    # Dashboard: Exhibition Events
    path('dashboard/exhibition-events/', views.dashboard_manage_exhibition_events, name='dashboard_manage_exhibition_events'),
    path('dashboard/exhibition-events/add/', views.dashboard_add_exhibition_event, name='dashboard_add_exhibition_event'),
    path('dashboard/exhibition-events/edit/<int:pk>/', views.dashboard_edit_exhibition_event, name='dashboard_edit_exhibition_event'),
    path('dashboard/exhibition-events/delete/<int:pk>/', views.dashboard_delete_exhibition_event, name='dashboard_delete_exhibition_event'),

    # Dashboard: Instagram Posts
    path('dashboard/instagram-posts/', views.dashboard_manage_instagram_posts, name='dashboard_manage_instagram_posts'),
    path('dashboard/instagram-posts/add/', views.dashboard_add_instagram_post, name='dashboard_add_instagram_post'),
    path('dashboard/instagram-posts/edit/<int:pk>/', views.dashboard_edit_instagram_post, name='dashboard_edit_instagram_post'),
    path('dashboard/instagram-posts/delete/<int:pk>/', views.dashboard_delete_instagram_post, name='dashboard_delete_instagram_post'),

    # Dashboard: Subscribers
    path('dashboard/subscribers/', views.dashboard_manage_subscribers, name='dashboard_manage_subscribers'),
    path('dashboard/subscribers/send-newsletter/', views.dashboard_send_newsletter, name='dashboard_send_newsletter'),
    path('dashboard/subscribers/delete/<int:pk>/', views.dashboard_delete_subscriber, name='dashboard_delete_subscriber'),
    path('career/', views.career, name='career'),
    path('career/<int:pk>/', views.job_detail, name='job_detail'),
    
    path('dashboard/job-openings/', views.dashboard_manage_job_openings, name='dashboard_manage_job_openings'),
    path('dashboard/job-openings/add/', views.dashboard_add_job_opening, name='dashboard_add_job_opening'),
    path('dashboard/job-openings/edit/<int:pk>/', views.dashboard_edit_job_opening, name='dashboard_edit_job_opening'),
    path('dashboard/job-openings/delete/<int:pk>/', views.dashboard_delete_job_opening, name='dashboard_delete_job_opening'),

    path('dashboard/job-applications/', views.dashboard_manage_job_applications, name='dashboard_manage_job_applications'),
    path('dashboard/job-applications/view/<int:pk>/', views.dashboard_view_job_application, name='dashboard_view_job_application'),
    path('dashboard/job-applications/delete/<int:pk>/', views.dashboard_delete_job_application, name='dashboard_delete_job_application'),

    path('contact-us/', views.contact_us, name='contact'),
    
    path('dashboard/contact-messages/', views.dashboard_manage_contact_messages, name='dashboard_manage_contact_messages'),
    path('dashboard/contact-messages/view/<int:pk>/', views.dashboard_view_contact_message, name='dashboard_view_contact_message'),
    path('dashboard/contact-messages/delete/<int:pk>/', views.dashboard_delete_contact_message, name='dashboard_delete_contact_message'),
    path('dashboard/email-configuration/', views.dashboard_email_configuration, name='dashboard_email_configuration'),

    # Public Legal & Gallery Pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('book-expo-meeting/', views.book_expo_meeting, name='book_expo_meeting'),

    # Dashboard: Expo Meetings
    path('dashboard/expo-bookings/', views.dashboard_manage_expo_bookings, name='dashboard_manage_expo_bookings'),
    path('dashboard/expo-bookings/status/<int:pk>/', views.dashboard_expo_booking_status, name='dashboard_expo_booking_status'),
    path('dashboard/expo-bookings/delete/<int:pk>/', views.dashboard_delete_expo_booking, name='dashboard_delete_expo_booking'),

    # Dashboard: Unified B2B Leads Manager
    path('dashboard/leads/', views.dashboard_manage_leads, name='dashboard_manage_leads'),
    path('dashboard/leads/export/', views.dashboard_export_leads_csv, name='dashboard_export_leads_csv'),

    # Dashboard: Operational Tools & Analytics
    path('dashboard/analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    path('dashboard/tools/compressor/', views.dashboard_compressor, name='dashboard_compressor'),
    path('dashboard/tools/compressor/save/', views.dashboard_compressor_save, name='dashboard_compressor_save'),
    path('dashboard/tools/pdf-thumbnails/', views.dashboard_pdf_thumbnails, name='dashboard_pdf_thumbnails'),
    path('dashboard/tools/pdf-thumbnails/save/', views.dashboard_pdf_thumbnail_save, name='dashboard_pdf_thumbnail_save'),
    path('dashboard/tools/sitemap/', views.dashboard_sitemap, name='dashboard_sitemap'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
