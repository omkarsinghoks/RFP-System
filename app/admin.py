from django.contrib import admin
from .models import RFPUserDetails, RFPVendorDetail,RFPCategories

@admin.register(RFPUserDetails)
class RFPUserDetailsAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(RFPVendorDetail)
class RFPVendorDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile_number', 'revenue', 'no_of_employee']
    
@admin.register(RFPCategories)
class RFPCategoriesAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'status', 'action']

  