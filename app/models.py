from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class RFPUserDetails(AbstractUser):
    USER_TYPE_CHOICES = [
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,  
        default='vendor', 
          
    )
class RFPVendorDetail(models.Model):
    user = models.ForeignKey(RFPUserDetails, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)  
    revenue = models.IntegerField()
    no_of_employee = models.IntegerField()
    gst_number = models.CharField(max_length=20)
    pan_no = models.CharField(max_length=20)
    categories = models.ManyToManyField('RFPCategories', blank=True)
    vendor_status = models.CharField(
        max_length=10, 
        choices=(('approve', 'Approve'), ('Rejected', 'Rejected')),
        default='Rejected' 
    )
    def __str__(self):
        return f"{self.user.username}"
   
class RFPCategories(models.Model):
    
    category_name = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=10, choices=(('active', 'Active'), ('inactive', 'Inactive')))
    action= models.CharField(max_length=15, choices=(('Deactivate', 'Deactivate'), ('Activate', 'Activate')))
    def __str__(self):
        return self.category_name




class RFPList(models.Model):
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    category = models.ForeignKey(RFPCategories, on_delete=models.CASCADE)
    last_date = models.DateField(default=now, auto_now=False)
    min_amount = models.IntegerField()
    max_amount = models.IntegerField()
    quanity = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=(('OPEN', 'Open'), ('CLOSE', 'Close')),
        default='OPEN'
    )
    # admin=models.ForeignKey(RFPUserDetails, on_delete=models.CASCADE, related_name='admin')
    
    

class RFPQuotes(models.Model):
    rfp = models.ForeignKey(RFPList, on_delete=models.CASCADE)
    vendor = models.ForeignKey(RFPVendorDetail, on_delete=models.CASCADE)
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    item_description = models.TextField()
   
