from django.shortcuts import render, get_object_or_404

from products.models import Product
from .models import Category, CategoryImage
# Create your views here.
def category_view(request):
    cat = Category.objects.all()
    cat_image = CategoryImage.objects.filter(category_id__in =cat)[:4]
    
    context = {
        
        "cat_image": cat_image
    }
    return render(request, 'category/category_list.html', context)



def category_product_list(request, slug):
    categories = Category.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    
    context = {
        "products": products,
        'category': category,
        'categories': categories,
    }
    
    return render(request, 'category/category_product_list.html', context)
