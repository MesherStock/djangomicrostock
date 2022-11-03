from itertools import chain
from django.http import Http404
from django.shortcuts import render
from .forms import ProductForm
from vendors.mixins import VendorMixin
from microstock.mixins import MultiSlugMixin
from .mixins import ProductUpdateMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

class ProductCreateView(VendorMixin,CreateView):
    model=Product
    form_class = ProductForm
    template_name = 'products/create_view.html'
    success_url = '/'
    
    def form_valid(self, form):
        vendor = self.get_vendor()
        form.instance.seller = vendor
        data = super(ProductCreateView, self).form_valid(form)
        print(data)
        
        return data
    

def product_detail(request, slug):
    obj = Product.objects.filter(slug=slug)
    product = None
    if obj.exists():
        product = obj.first()
    
    related_product = Product.objects.filter(category=product.category).exclude(slug=product.slug)
    
    context = {
        'product': product,
        'related_product': related_product,
    }
    return render(request, 'products/product_detail.html', context)


def search_view(request, *args, **kwargs):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
    obj = Product.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(category__title__icontains=q)).order_by('id')
    results = list(chain(obj))
    paginator = Paginator(results, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    
    context = {
        'results': paged_products,
        'obj': obj,
        'q': q
    }
    return render(request, "products/search_result.html", context)


        

class ProductUpdateView(ProductUpdateMixin,MultiSlugMixin,UpdateView):
    model=Product
    form_class = ProductForm
    template_name = 'products/update_view.html'
    success_url = '/'   

