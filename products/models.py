from email.policy import default
from unicodedata import category
from django.db import models
from vendors.models import Vendor
from category.models import Category
from .storage import ProtectedMedia
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
def download_media(instance, filename):
    return "%s/%s"%(instance.slug, filename)

class Product(models.Model):
    seller = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='download_media', null=True, blank=True)
    media = models.FileField(upload_to="download_media", storage=ProtectedMedia, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    featured = models.BooleanField(default=False)
    recent_product = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product:detail", args={self.slug})
    

def save_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    obj = Product.objects.filter(slug=slug)
    exists = obj.exists()
    if exists:
        new_slug = "%s/%s"%(slug, obj.first().id)
        return save_slug(instance, new_slug=new_slug)
    return slug

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug =  save_slug(instance)  

pre_save.connect(product_pre_save_receiver, sender=Product)   
    


