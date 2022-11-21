from microstock.mixins import LoginRequiredMixin
from .models import Vendor
from products.models import Product
from orders.models import OrderProduct

class VendorMixin(LoginRequiredMixin, object):
    vendor = None
    def get_vendor(self):
        seller = self.request.user
        vendors = Vendor.objects.filter(seller=seller)
        if vendors.exists() and vendors.count() == 1:
            self.vendor = vendors.first()
            return vendors.first()
        return None
    
    def get_product(self):
        vendor = self.get_vendor()
        products = Product.objects.filter(seller=vendor)
        self.product = products
        return products
    
    def get_transaction(self):
        product = self.get_product()
        transactions = OrderProduct.objects.filter(product__in=product)
        return transactions
        