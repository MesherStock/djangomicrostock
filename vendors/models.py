from email.policy import default
from django.db import models
from accounts.models import User
from django.urls import reverse

# Create your models here.
class Vendor(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.seller.first_name
    
    def get_absolute_url(self):
        view_name = 'product:vendor_detail'
        return reverse(view_name, kwargs={"vendor_name":self.seller.username})
    
    
