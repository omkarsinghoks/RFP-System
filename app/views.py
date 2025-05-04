from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .forms import RFPUserDetailsForm, RFPVendorDetailForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RFPUserDetails,RFPVendorDetail,RFPCategories
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .models import RFPUserDetails, RFPVendorDetail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import RFPCategories, RFPList,RFPQuotes,RFPVendorDetail




def registerAdmin(request):
    
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        field_errors = {}
        if not first_name:
            field_errors['first_name'] = "Please enter your first name."
        elif len(first_name) < 2:
            field_errors['first_name'] = "First name must be at least 2 characters long."
        
        # Validate last name
        if not last_name:
            field_errors['last_name'] = "Please enter your last name."

        # Validation Checks
        if not email:
            field_errors['email'] = "Please enter your email."
        elif RFPUserDetails.objects.filter(email=email).exists():
            field_errors['email'] = "Email is already registered."
        elif email and '@' not in email:
            field_errors['email'] = "Please enter a valid email address."  
        elif email and '.' not in email.split('@')[-1]:
            field_errors['email'] = "Please enter a valid email address." 
        if not password:
            field_errors['password'] = "Please enter your password."
        elif len(password) < 8:
            field_errors['password'] = "Password must be at least 8 characters long."
        if not confirm_password:
            field_errors['confirm_password'] = "Please confirm your password."
        elif password != confirm_password:
            field_errors['confirm_password'] = "Passwords do not match."
        try:
            if not field_errors:    
                RFPUserDetails.objects.create(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=make_password(password),  
                    user_type='admin'
                )
                subject = "Admin Registration Successful"
                message = render_to_string('app/admin_registration_email.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                })
                from_email = "oksi6189@gmail.com"  
                recipient_list = [email]

                email = EmailMessage(subject, message, from_email, recipient_list)
                email.content_subtype = "html"  # Send as HTML
                email.send()
                messages.success(request, "Admin registered successfully!") 
                return redirect('registerAdmin') 
            else:    
                # messages.error(request, "Please fill all the required fields.")
                return render(request, 'app/adminRegister.html', {'field_errors': field_errors ,"form_data": request.POST})
             
        except Exception as e: 
            messages.error(request, f"Error occurred: {e}")
            return redirect('registerAdmin')

    return  render(request, 'app/adminRegister.html')


def registerVendor(request):
    categories = RFPCategories.objects.filter(status__iexact='active')
    ''' used t register the vendor 
        and category field will show from RFPCategotys 
    '''

    if request.method == 'POST':
        
        print(request.POST)
       
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        revenue = request.POST.get('revenue')
        no_of_employees = request.POST.get('no_of_employees')
        gst_no = request.POST.get('gst_no')
        pan_no = request.POST.get('pan_no')
        mobile_number = request.POST.get('mobile_number')
        category_ids = request.POST.getlist('categories')
        field_errors = {}
        if not first_name:
            field_errors['first_name'] = "Please enter your first name."
        elif len(first_name) < 2:
            field_errors['first_name'] = "First name must be at least 2 characters long."
        
       
        if not last_name:
            field_errors['last_name'] = "Please enter your last name."

       
        if not email:
            field_errors['email'] = "Please enter your email."
        elif RFPUserDetails.objects.filter(email=email).exists():
            field_errors['email'] = "Email is already registered."
        elif email and '@' not in email:
            field_errors['email'] = "Please enter a valid email address."  
        elif email and '.' not in email.split('@')[-1]:
            field_errors['email'] = "Please enter a valid email address." 
        if not password:
            field_errors['password'] = "Please enter your password."
        elif len(password) < 8:
            field_errors['password'] = "Password must be at least 8 characters long."
        if not confirm_password:
            field_errors['confirm_password'] = "Please confirm your password."
        elif password != confirm_password:
            field_errors['confirm_password'] = "Passwords do not match."
        if not revenue:
            field_errors['revenue'] = "Please enter your revenue."
        elif not revenue.isdigit() or int(revenue) <= 0:
            field_errors['revenue'] = "Revenue must be a positive number."

        # Validate number of employees
        if not no_of_employees:
            field_errors['no_of_employees'] = "Please enter the number of employees."
        elif not no_of_employees.isdigit() or int(no_of_employees) <= 0:
            field_errors['no_of_employees'] = "Number of employees must be a positive number."

        # Validate GST number
        if not gst_no:
            field_errors['gst_no'] = "Please enter your GST number."
        elif len(gst_no) != 15:
            field_errors['gst_no'] = "GST number must be 15 characters long."
        if not pan_no:
            field_errors['pan_no'] = "Please enter your PAN number."
        elif len(pan_no) != 10:
            field_errors['pan_no'] = "PAN number must be 10 characters long."

        # Validate mobile number
        if not mobile_number:
            field_errors['mobile_number'] = "Please enter your mobile number."
        elif not mobile_number.isdigit() or len(mobile_number) != 10:
            field_errors['mobile_number'] = "Mobile number must be a 10-digit number."

        # Validate categories
        if not category_ids:
            field_errors['categories'] = "Please select at least one category."


       

        if field_errors:
             return render(request, 'app/vendor_register.html', {'categories': categories, 'field_errors': field_errors , 'form_data': request.POST})
        if not all([first_name, last_name, email, password, confirm_password, revenue,
                    no_of_employees, gst_no, pan_no, mobile_number, category_ids]):
            messages.error(request, "All fields are required.")
            return redirect('registerVendor' )

        
        try:
            # print(f"First Name: {first_name}")
            # print(f"Last Name: {last_name}")
            # print(f"Email: {email}")
            # print(f"Password: {password}")
            user = RFPUserDetails.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                 username=email,
                password=make_password(password),  
                user_type='vendor'
            )
            
            

           
            vendor_detail= RFPVendorDetail.objects.create(
                user=user,
                revenue=revenue,
                 no_of_employee=no_of_employees,
                gst_number=gst_no,
                pan_no=pan_no,
                mobile_number=mobile_number,
                
            )
            
            categories = RFPCategories.objects.filter(id__in=category_ids)  # Ensure valid IDs
            vendor_detail.categories.set(categories)

            messages.success(request, "Vendor registered successfully!")
            subject = "Vendor Registration Successful"
            message = render_to_string('app/vendor_registration_email.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                })
            from_email = "oksi6189@gmail.com"  # Replace with your email
            recipient_list = [email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = "html"  # Send as HTML
            email.send()
            return redirect('registerVendor')

        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect('registerVendor')
   
    return render(request, 'app/vendor_register.html', {'categories': categories})









# def login(request):

#     if 'success_message' in request.session:
#         del request.session['success_message']
#     return render(request, 'app/login.html')
  
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        try:
            if user is not None:
                # Check if the user is a vendor
                vendor_detail = RFPVendorDetail.objects.filter(user_id=user.id).first()
                if vendor_detail:
                    # Check vendor status
                    if vendor_detail.vendor_status.lower() == 'approve':
                        login(request, user)
                        print("Login successful as Vendor")
                        return redirect('vendor_page')
                    else:
                        messages.error(request, "Your account is not approved. Please contact the admin.")
                        return redirect('login')
                else:
                    # If the user is not a vendor, assume they are an admin
                    login(request, user)
                    print("Login successful as Admin")
                    return redirect('admin_page')
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect('login')
    return render(request, 'app/login.html')
    
@login_required
def admin_page(request):
    return render(request, 'app/admin_page.html')

@login_required
def vendor_page(request):
    return render(request, 'app/vendor_page.html')


def logout_view(request):
    # Clear the session and redirect to login page
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect('login') 


# def send_reset_email(request):
#     try:
#         subject = "Test Email from Django"
#         message = "Hello, this is a test email from Django."
#         from_email = "oksi6189@gmail.com"  # Must match EMAIL_HOST_USER
#         recipient_list = ["karan.bisht@velsof.com"]
#         print("Sending email...")
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         return render(request, 'app/login.html')
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         messages.error(request, f"Error occurred: {e}")
#         return render(request, 'app/login.html')




def send_reset_email(request):
    try:
        email = request.POST.get('email')

        # Check if the email exists in the database
        

        if not RFPUserDetails.objects.filter(email=email).exists():
            messages.error(request, "No user found with this email address.")
            return render(request, 'app/forgot_password.html')

        # Generate the reset link
        reset_link = f"http://127.0.0.1:8000/reset-password/{email}/"

        # Render the email content using an HTML template
        subject = "Password Reset Request"
        message = render_to_string('app/reset_email_template.html', {
            'reset_link': reset_link,
            'user_email': email,
        })

        # Send the email
        from_email = "oksi6189@gmail.com"  # Must match EMAIL_HOST_USER
        recipient_list = [email]
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = "html"  # Set the email content type to HTML
        email_message.send()

        messages.success(request, "Password reset email sent successfully!")
        return render(request, 'app/forgot_password.html')
    except Exception as e:
        print(f"Error sending email: {e}")
        messages.error(request, f"Error occurred: {e}")
        return render(request, 'app/login.html')


def reset_password(request, email):
    """
   View to handle password reset. 
    """
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'app/reset_password.html', {'email': email})

        try:
            user =RFPUserDetails.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully! You can now log in.")
            return redirect('login')
        except user.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('forgotPassword')

    return render(request, 'app/reset_password.html', {'email': email})







@login_required
def rfp_list(request): 
    '''
    Display the list of RFPs (Request for Proposals).
        '''
    try:
        rfp_list = RFPList.objects.all()
        return render(request, 'app/rfp_list.html', {'rfp_list': rfp_list})
    except Exception as e:
        print(f'Error in rfp_list: {e}')
    return render(request, 'app/rfp_list.html')



def registerVendor1(request):
    return render(request, 'app/vendor_register.html')


def forgotPassword(request):
    return render(request, 'app/forgot_password.html')

@login_required
def vendor_list(request):
    userDetails = RFPUserDetails.objects.filter(user_type='vendor') 
    vendorDetails = RFPVendorDetail.objects.all()

    
    combined_data = []
    for user in userDetails:
        vendor_detail = vendorDetails.filter(user=user).first()  # Get the 
        combined_data.append({
            'user': user,
            'vendor_detail': vendor_detail
        })

    
    return render(request, 'app/vendor_list.html', {'combined_data': combined_data})

@login_required
def toggle_vendor_status(request, vendor_id):
    """
    View to toggle the vendor status between 'Approve' and 'Rejected'.
    """
    try:
        # Get the vendor detail object
        vendor_detail = get_object_or_404(RFPVendorDetail, id=vendor_id)

        # Toggle the status
        if vendor_detail.vendor_status.lower() == 'rejected':
            vendor_detail.vendor_status = 'approve'
            # messages.success(request, f"Vendor {vendor_detail.user.first_name} approved successfully.")
        else:
            vendor_detail.vendor_status = 'Rejected'
            # messages.success(request, f"Vendor {vendor_detail.user.first_name} rejected successfully.")

        # Save the updated status
        vendor_detail.save()

    except Exception as e:
        messages.error(request, f"Error occurred: {e}")

    # Redirect back to the vendor list page
    return redirect('vendor_list')

@login_required
def addCategory(request):   
    try:
            categories= RFPCategories.objects.filter(status__iexact='active')
            return render(request, 'app/add_category.html' ,{'categories':categories}) 
    except Exception as e:
        print(f'Error in addCategory: {e}')
        messages.error(request, f"Error occurred: {e}")


@login_required
def rpf_create(request):
    '''
    Create a new RFP (Request for Proposal) entry.
    Get the category ID from the add category page, find vendors in that category, and pass them to the template.
    '''
    try:
        if request.method == 'POST':
           
            category_id = request.POST.get('category')  

            
            category = RFPCategories.objects.get(id=category_id)

            
            vendors = RFPVendorDetail.objects.filter(categories=category)

            
            return render(request, 'app/rfp_create.html', {'category_id': category_id, 'vendors': vendors})
        else:
           
            return render(request, 'app/rfp_create.html', {'category_id': 1, 'vendors': []})
    except Exception as e:
        print(f'Error in rpf_create: {e}')
        messages.error(request, f"Error occurred: {e}")
        return render(request, 'app/rfp_create.html', {'category_id': 1, 'vendors': []})
    
@login_required
def rfp_object_create(request):
    '''
    Create a new RFP (Request for Proposal) entry.
    Get the category ID from the form and store it in the RFPList table.
    '''
    try:
        if request.method == 'POST':
           
            item_name = request.POST.get('item_name')
            item_description = request.POST.get('item_description')
            category_id = request.POST.get('category_id')  
            min_amount = request.POST.get('min_price')
            max_amount = request.POST.get('max_price')
            quantity = request.POST.get('quantity')
            last_date = request.POST.get('last_date')
            vendor_ids = request.POST.getlist('vendor') 

            field_errors = {}

            if not item_name:
                field_errors['item_name'] = "Please enter the item name."
            if not item_description:
                field_errors['item_description'] = "Please enter the item description."
            if not category_id or not category_id.isdigit():
                field_errors['category_id'] = "Invalid category selected."
            if not min_amount or not min_amount.isdigit():
                field_errors['min_price'] = "Please enter a valid minimum amount."
            if not max_amount or not max_amount.isdigit():
                field_errors['max_price'] = "Please enter a valid maximum amount."
            if not quantity or not quantity.isdigit():
                field_errors['quantity'] = "Please enter a valid quantity."
            if not vendor_ids:
                field_errors['vendor'] = "Please Selecte Vendor."
            if not last_date:
                field_errors['last_date'] = "Please enter a last_date."


            # If there are validation errors, return them to the template
            if field_errors:
                # Fetch vendors associated with the selected category
                vendors = RFPVendorDetail.objects.filter(categories__id=category_id).distinct()
                return render(request, 'app/rfp_create.html', {
                    'field_errors': field_errors,
                    'vendors': vendors,
                    'selected_vendors': vendor_ids,  # Pass selected vendors back to the template
                    'category_id': category_id,  # Preserve category_id if needed
                })

            category = RFPCategories.objects.get(id=category_id) 
            
            rfp = RFPList.objects.create(
                item_name=item_name,
                item_description=item_description,
                category=category, 
                min_amount=min_amount,
                max_amount=max_amount,
                quanity=quantity,
                last_date=last_date,
                # admin=request.user  
            )
            # mail sending 
            vendors = RFPVendorDetail.objects.filter(categories__id__in=category_id).distinct()
            for vendor in vendors:
                subject = f"New RFP: {item_name}"
                message = render_to_string('app/vendor_rfp_notification.html', {
                    'vendor': vendor,
                    'rfp': rfp,
                })
                from_email = "oksi6189@gmail.com"  
                recipient_list = [vendor.user.email]

                email = EmailMessage(subject, message, from_email, recipient_list)
                email.content_subtype = "html"  
                email.send()

            messages.success(request, "RFP created successfully!")
            return redirect('rfp_list') 

        else:
            return render(request, 'app/rfp_create.html')  
    except Exception as e:
        print(f'Error in rfp_object_create: {e}')
        messages.error(request, f"Error occurred: {e}")
        return render(request, 'app/rfp_create.html')
    
@login_required
def category(request): 
    '''     
    Display the list of categories.

    '''
    try:
        categories = RFPCategories.objects.all()
        return render(request, 'app/category_page.html', {'categories': categories})
    except Exception as e:
        print(f'Error in category: {e}')
        messages.error(request, f"Error occurred: {e}")
        return render(request, 'app/category.html')


@login_required
def toggle_category_status(request, category_id):
    
    category = get_object_or_404(RFPCategories, id=category_id)

    
    if category.status == "Active":
        category.status = "Inactive"
    else:
        category.status = "Active"

   
    category.save()

    return redirect('category') 


@login_required
def toggle_rfp_status(request, rfp_id):
    # Get the RFP object
    rfp = get_object_or_404(RFPList, id=rfp_id)

    # Toggle the status
    if rfp.status == 'OPEN':
        rfp.status = 'CLOSE'
    else:
        rfp.status = 'OPEN'

    # Save the updated status
    rfp.save()

    
    return redirect('rfp_list')








@login_required 
def rfpQuotes(request):
    try:
        quotes = RFPQuotes.objects.select_related('rfp', 'vendor').all()

        return render(request, 'app/rfp_quotes_admin.html', {'quotes': quotes})
    except Exception as e:
        print(e)
        return render(request,'app/rfp_quotes_admin.html')

def rfp_quote_vendor(request):
    try:
        rfp_list = RFPList.objects.all()
        return render(request, 'app/rfp_quote_vendor.html', {'rfp_list': rfp_list})
    except Exception as e:
        print(f'Error in rfp_list: {e}')
        messages.error(request, f'error {e}')
        return render(request, 'app/rfp_list.html')

@login_required    
def rfp_create_vendor(request, rfp_id):
    """
    View to render the RFP creation form for vendors.
    """
    try:
        rfp = get_object_or_404(RFPList, id=rfp_id)

        return render(request, 'app/rfp_create_vendor.html', {'rfp': rfp})
    except Exception as e:
        print(e)





@login_required
def create_category(request):
    '''
    View to add a new category.
    to create a new object into category  model
    '''
    field_errors = {}
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        status = request.POST.get('status')

        
        if not category_name:
            field_errors['category_name'] = "Category name is required."
        elif RFPCategories.objects.filter(category_name=category_name).exists():
            field_errors['category_name'] = "Category name already exists."

        if not status or status not in ['Active', 'Inactive']:
            field_errors['status'] = "Invalid status selected."

        if field_errors:
            return render(request, 'app/create_category.html', {'field_errors': field_errors})

        
        try:
            RFPCategories.objects.create(
                category_name=category_name,
                status=status,
                action='Deactivate' if status == 'Active' else 'Activate'
            )
            # messages.success(request, "Category added successfully!")
            return redirect('category')  
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return render(request, 'app/add_category.html')

    return render(request, 'app/create_category.html')

@login_required
def create_category_page(request):
     return render(request, 'app/create_category.html')






@login_required
def submit_rfp_quote(request, rfp_id):
    """
    View to handle the submission of RFP quotes by vendors.
    Send the mail to the admin or stakeholders.
    """
    try:
        print("Logged-in user:", request.user)
        print(rfp_id)
        vendor = RFPVendorDetail.objects.filter(user=request.user).first()
        print("Vendor details:", vendor)
        rfp = get_object_or_404(RFPList, id=rfp_id, status='OPEN')
    except Exception as e:
        print('error', e)
        messages.error(request, "The requested RFP is not available or is closed.")
        return redirect('rfp_quote_vendor')

    if request.method == 'POST':
        vendor_price = request.POST.get('vendor_price')
        quantity = request.POST.get('quantity')
        item_description = request.POST.get('item_description')
        field_errors = {}
        if not vendor_price:
            field_errors['vendor_price'] = "Vendor price is required."
        elif not vendor_price.isdigit() or int(vendor_price) <= 0:
            field_errors['vendor_price'] = "Vendor price must be a positive number."

        if not quantity:
            field_errors['quantity'] = "Quantity is required."
        elif not quantity.isdigit() or int(quantity) <= 0:
            field_errors['quantity'] = "Quantity must be a positive number."

        if not item_description:
            field_errors['item_description'] = "Item description is required."
        if field_errors:
            return render(request, 'app/rfp_create_vendor.html',{'rfp': rfp, 'field_errors': field_errors})

        try:
            # Save the quote to the database
            quote = RFPQuotes.objects.create(
                rfp=rfp,
                vendor=vendor,
                vendor_price=vendor_price,
                quantity=quantity,
                item_description=item_description
            )

            # Fetch admin emails dynamically
            admin_emails = RFPUserDetails.objects.filter(user_type='admin').values_list('email', flat=True)
            recipient_list = list(admin_emails)

            # Send email notification
            subject = f"New Quote Submitted for RFP: {rfp.item_name}"
            message = render_to_string('app/quote_notification.html', {
                'rfp': rfp,
                'vendor': vendor,
                'quote': quote,
            })
            from_email = "oksi6189@gmail.com"  # Replace with your email

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = "html"  # Set the email content type to HTML
            print('mail send successfully')
            email.send()

            messages.success(request, "Quote submitted successfully! An email notification has been sent.")
            return redirect('rfp_quote_vendor')
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect('submit_rfp_quote', rfp_id=rfp_id)

    return render(request, 'app/rfp_create_vendor.html', {'rfp': rfp})





def rfp_quotes_admin(request):
    """
    View to display all submitted RFP quotes in the admin section.
    """
    # Fetch all RFP quotes
    quotes = RFPQuotes.objects.select_related('rfp', 'vendor').all()

    return render(request, 'app/rfp_quotes_admin.html', {'quotes': quotes})








# categories = RFPCategories.objects.filter(status__iexact='active') case insensitive 