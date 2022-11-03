from django.urls import path
from products.views import (ProductCreateView,
                            ProductUpdateView
            
                            )
from .import views

app_name = 'product'
urlpatterns = [
    path('product/create/', ProductCreateView.as_view(), name='create'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='update'),
    path('product/<slug:slug>/', views.product_detail, name='detail'),
    path('search/', views.search_view, name='search'),
    
    
]