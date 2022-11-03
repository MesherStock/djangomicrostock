from vendors.mixins import VendorMixin
from django.http import Http404



class ProductUpdateMixin(VendorMixin, object):
    def get_object(self, *args, **kwargs):
        seller = self.get_vendor()
        obj = super(ProductUpdateMixin, self).get_object(*args, **kwargs)
        try:
            obj.seller == seller
        except:
            raise Http404
        
        if obj.seller == seller:
            return obj
        else:
            raise Http404