from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'email', 'product_name', 'created_at')
    list_filter = ('created_at', 'product_name')
    search_fields = ('full_name', 'company', 'email', 'message')
    readonly_fields = ('full_name', 'company', 'email', 'product_name', 'message', 'created_at')

    def has_add_permission(self, request):
        return False  # Enquiries are created via the frontend form, not admin

    def has_change_permission(self, request, obj=None):
        return False  # Enquiries should be read-only
