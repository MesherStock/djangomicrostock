from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, prod_id):
    prod = Product.objects.get(id=prod_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    
    try:
        cartitem = CartItem.objects.get(prod=prod, cart=cart) 
        cartitem.quantity += 1
        cartitem.save()
    except CartItem.DoesNotExist:
        cartitem = CartItem.objects.create(prod=prod, quantity=1,cart=cart)
        cartitem.save()
        return redirect("cart:cart")
    


def cart(request):
    return render(request, 'carts/cart.html')
