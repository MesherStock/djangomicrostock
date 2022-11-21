from email.policy import default
from django.db import models
from django.urls import reverse
# Create your models here.
def categ_media(instance, filename):
    return "%s/%s"%(instance.slug, filename)


class Category(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    slug = models.SlugField()
    order = models.BooleanField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def get_url(self):
        return reverse("category:category_view")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"



class CategoryImage(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    image = models.ImageField(upload_to=categ_media)
    slug = models.SlugField()
    featured_image = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add = False, auto_now=True)

    def __str__(self):
        return self.title
    
    
    

    
    
    def get_cat_url(self):
        return reverse('category:category', kwargs={"slug":self.slug})
