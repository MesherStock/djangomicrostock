from django.urls import path
from products.views import (ProductCreateView,
                            ProductUpdateView,
                            VendorListView
                            )
from .import views
from django.views.generic.base import RedirectView
app_name = 'product'
urlpatterns = [
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('search/result', views.search_view, name='search'),
    path("vendor/<vendor_name>/", VendorListView.as_view(), name='vendor_detail'),
    path('vendor/product/', RedirectView.as_view(pattern_name='category:category_view'), name='vendor_list'),

    
    
]