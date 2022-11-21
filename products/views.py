from itertools import chain
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import ProductForm
from vendors.mixins import VendorMixin
from microstock.mixins import MultiSlugMixin
from .mixins import ProductUpdateMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category, CategoryImage

from django.views.generic.list import ListView
from vendors.models import Vendor
# Create your views here.

class ProductCreateView(VendorMixin,CreateView):
    model=Product
    form_class = ProductForm
    template_name = 'products/create_view.html'
    success_url = '/vendor/product/list'
    
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
    
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(user=request.user, product=product).exists()
    
    else:    
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    
    related_product = Product.objects.filter(category=product.category).exclude(slug=product.slug)
    cat = Category.objects.all()
    cat_image = CategoryImage.objects.filter(category_id__in =cat)[:4]
    
    context = {
        'product': product,
        'related_product': related_product,
        'in_cart': in_cart,
        'cat': cat,
        'cat_image': cat_image
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
    success_url = '/vendor/product/list'   



class VendorListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    
    
    def get_object(self, *args, **kwargs):
        seller_name = self.kwargs.get("vendor_name")
        seller = get_object_or_404(Vendor, seller__username=seller_name)
        return seller
    
    def get_context_data(self, *args,**kwargs):
        context =super(VendorListView, self).get_context_data(*args,**kwargs)
        context['vendor_name'] = str(self.get_object().seller.username)
        
        return context
    
    def get_queryset(self, **kwargs):
        seller = self.get_object()
        qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
        return qs







# class VendorListView(ListView):
#     model = Product
#     template_name = "products/product_list.html"



#     def get_object(self, *args, **kwargs):
#         username = self.kwargs.get("vendor_name")
#         seller = get_object_or_404(Vendor, seller__username=username)
#         return seller


#     def get_context_data(self, **kwargs):
#         context = super(VendorListView, self).get_context_data(**kwargs)
#         context["vendor_name"] = str(self.get_object().seller.username)
#         return context

#     def get_queryset(self, **kwargs):
#         seller = self.get_object()
#         qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
#         # qs = qs.filter(is_featured=True)
#         query = self.request.GET.get("q", "")
#         if query:
#             qs = qs.filter(Q(title__icontains=query)|Q(description__icontains=query))
#         results = list(chain(qs))
#         return results