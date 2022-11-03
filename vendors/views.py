from genericpath import exists
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from vendors.mixins import VendorMixin
from .forms import VendorForm
from microstock.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .models import Vendor

# Create your views here.

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
        
        else:
            pass
        return render(request, "vendors/dashboard.html", context)
    
    def form_valid(self, form):
        data = super(VendorDashBoard, self).form_valid(form)
        Vendor.objects.create(seller=self.request.user)
        return data
