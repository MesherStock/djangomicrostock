from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product
from category.models import Category, CategoryImage

def index(request):
    cat = Category.objects.all()
    cat_image = CategoryImage.objects.filter(category_id__in =cat)[:4]
    
    context = {
        
        "cat_image": cat_image
    }
    return render(request, 'index.html', context)