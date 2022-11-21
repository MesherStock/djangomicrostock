from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, prod_id):
    user = request.user
    product = Product.objects.get(id=prod_id)
    if user.is_authenticated:
        cart_item_exist = CartItem.objects.filter(product=product, user=user).exists()
        if cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, user=user)
        
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=user)
            cart_item.save()
        return redirect("cart:cart")
    else:
        try:
            cart = Cart.objects.get(cart_id =_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            cart_item.save()
        return redirect("cart:cart")


def remove_cart(request, prod_id, cart_item_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=prod_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))    
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart:cart")

def cart(request, cart_items = None, total = 0):
    try:
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        
        else:
            cart = Cart.objects.get(cart_id =_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            
        tax_rate = Decimal(0.05)
        tax = (total * tax_rate)
        tax = Decimal("%.2f" %(tax))
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total

    }
    return render(request, 'carts/cart.html', context)



@login_required(login_url='account:login')
def checkout(request,cart_items = None, total = 0):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        
        else:
            cart = Cart.objects.get(cart_id =_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            
        tax_rate = Decimal(0.05)
        tax = (total * tax_rate)
        tax = Decimal("%.2f" %(tax))
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total

    }
    return render(request, "carts/checkout.html", context)
    
