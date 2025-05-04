from django.contrib import admin
from django.urls import path
from app.views import login, registerAdmin, registerVendor, forgotPassword,admin_page,login_view ,vendor_page,logout_view,send_reset_email,toggle_vendor_status ,vendor_list,rfp_list,addCategory ,rpf_create,rfp_object_create,category,rfpQuotes,toggle_category_status, toggle_rfp_status,rfp_quote_vendor, rfp_create_vendor,create_category,create_category_page, submit_rfp_quote,rfp_quotes_admin,reset_password

urlpatterns = [
     path('', login_view,name='login'),  
     path('register-admin/', registerAdmin ,name='registerAdmin'),   
     path('register-vendor/', registerVendor ,name='registerVendor'),  
     path('forgotPassword/',forgotPassword,name='forgotPassword'),
     path('admin-page/',admin_page,name='admin_page'), 
     path('vendor-page/',vendor_page,name='vendor_page'), 
     path('logout/', logout_view, name='logout'),
     path('email/', send_reset_email, name='email'),
     path('vendor-list/', vendor_list, name='vendor_list'),
     path('toggle-vendor-status/<int:vendor_id>/', toggle_vendor_status, name='toggle_vendor_status'),
     path('rfp-list/', rfp_list, name='rfp_list'),
     path('add-category/', addCategory , name='addCategory'),
     path('rpf-create/', rpf_create, name='rpf_create'),
     path('rfp-object-create/', rfp_object_create, name='rfp_object_create'),
     path('category/', category, name='category'),
     path('rfp_quotes/', rfpQuotes, name='rfp_quotes'),
     path('toggle-category-status/<int:category_id>/', toggle_category_status, name='toggle_category_status'),
     path('toggle-rfp-status/<int:rfp_id>/', toggle_rfp_status, name='toggle_rfp_status'),
     path('rfp-quote-vendor/', rfp_quote_vendor ,name='rfp_quote_vendor'),
     path('rfp-create-vendor/<int:rfp_id>/', rfp_create_vendor, name='rfp_create_vendor'),
     path('create-category-page/',create_category_page, name='create-category-page'),
     path('create-category/',create_category, name='create_category'),
     path('submit-quote/<int:rfp_id>/', submit_rfp_quote, name='submit_rfp_quote'),
     path('admin/rfp-quotes/', rfp_quotes_admin, name='rfp_quotes_admin'),
     path('reset-password/<str:email>/', reset_password, name='reset_password'),

]

