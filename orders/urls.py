from django.urls import path

from .import views


app_name = 'order'

urlpatterns = [ 
             path('place_order', views.place_order, name='place_order'),
             path("payment", views.payment_view, name='payment'),
             path('success/', views.myorder_view, name='success'),
             path('order/<int:order_id>/download', views.order_download, name='download')
            
               ]