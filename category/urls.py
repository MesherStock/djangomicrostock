from django.urls import path
from . import views

app_name ='category'
urlpatterns = [
    path('<slug:slug>/', views.category_product_list, name='category'),
    path('', views.category_view, name='category_view'),
]