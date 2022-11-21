from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductTab(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ['payment', 'product_price']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    inlines= [OrderProductTab,]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
