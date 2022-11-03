from django.urls import path
from vendors.views import VendorDashBoard
app_name ='vendor'

urlpatterns = [ 
    path('', VendorDashBoard.as_view(), name='dashboard')
]