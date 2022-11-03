from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('account/', include('accounts.urls', namespace='account') ),
    path('category/', include('category.urls', namespace='category')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('', include('products.urls', namespace='product')),
    path('vendor/', include('vendors.urls', namespace='vendor'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



