
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import RFPUserDetails, RFPVendorDetail,RFPCategories


class RFPUserDetailsForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = RFPUserDetails
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        user_type = cleaned_data.get('user_type')


        errors = {}


        if first_name :
            errors['first_name'] = "First name is required"
        if last_name :
            errors['last_name'] = "Last name is required"
        if email:
            errors['email'] = "Email is required"
        if RFPUserDetails.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"
        if user_type:
            errors['user_type'] = "User type is required"
        
        # Password Strength Conditions
        if password:
            if len(password) < 8:
                errors['password'] = "Password must be at least 8 characters long."
            if not any(char.isdigit() for char in password):
                errors['password'] = "Password must contain at least one digit."

        # Password Match Condition
        if password and confirm_password and password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."

        # If any errors exist, raise a ValidationError
        if errors:
            raise ValidationError(errors)

        return cleaned_data

      
class RFPVendorDetailForm(forms.ModelForm):
    class Meta:
        model = RFPVendorDetail
        fields = [
            'mobile_number',
            'revenue',
            'no_of_employee',
            'gst_number',
            'pan_no',
            'categories'
        ]
class RFPCategoriesForm(forms.ModelForm):
    class Meta:
        model = RFPCategories
        fields = [
            'category_name',
            'status']