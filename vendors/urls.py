from django.urls import path
from vendors.views import (
    VendorDashBoard,
    VendorProduct,
    VendorTransactions
)
from products.views import (
    ProductCreateView,
    ProductUpdateView
)
app_name ='vendor'

urlpatterns = [ 
    path('', VendorDashBoard.as_view(), name='dashboard'),
    path('product/create/', ProductCreateView.as_view(), name='create'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='update'),
    path('product/list/', VendorProduct.as_view(), name="product_list"),
    path('transaction/', VendorTransactions.as_view(), name='transaction')
]