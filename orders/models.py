from django.db import models
from accounts.models import User
from products.models import Product
from django.urls import reverse
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.payment_id



class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
  
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete = models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    status = models.CharField(max_length=150, choices=STATUS, default='New')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ip =  models.CharField(max_length=100, null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.first_name
    
    

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.title
    
    @property
    def is_downloadable(self):
        if not self.product:
            return False
        
        if self.product.is_digital:
            return True
        return
    
    
    def get_download_url(self):
        view_name = "order:download"
        
        return reverse(view_name, kwargs={'order_id':self.pk})
    
    
    
