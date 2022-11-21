from genericpath import exists
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from vendors.mixins import VendorMixin
from .forms import VendorForm
from products.models import Product
from microstock.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from .models import Vendor
from orders.models import Order

# Create your views here.
class VendorProduct(VendorMixin, ListView):
    model = Product
    template_name = "vendors/product_list_view.html"
    
    def get_queryset(self, *args, **kwargs):
        qs = super(VendorProduct, self).get_queryset(*args, **kwargs)
        qs = qs.filter(seller=self.get_vendor())
        return qs


class VendorTransactions(VendorMixin, ListView):
    model = Order
    template_name = 'vendors/transaction_list.html'
    
    def get_queryset(self):
        return self.get_transaction




class VendorDashBoard(VendorMixin,FormMixin,View):
    form_class = VendorForm
    success_url = '/'


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwar):
        form = VendorForm()
        vendor = self.get_vendor()
        exists = vendor
        is_active = None
        context = {}
        if exists:
            is_active = vendor.is_active
        
        if not exists and not is_active:
            context['title'] = "Apply for Account"
            context['form'] = form
        elif exists and is_active:
            context['title'] = "Vendor Dashboard"
            context['products'] = self.get_product()[:4]
            context['transactions'] = self.get_transaction()[:4]
        
        else:
            pass
        return render(request, "vendors/dashboard.html", context)
    
    def form_valid(self, form):
        data = super(VendorDashBoard, self).form_valid(form)
        Vendor.objects.create(seller=self.request.user)
        return data
