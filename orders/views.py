import pathlib
from pathlib import Path
from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from decimal import Decimal
import datetime
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import json
# Create your views here.

def payment_view(request):
    
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(body)
    payment = Payment (
        user = request.user,
        payment_method = body['payment_method'],
        payment_id = body['transID'],
        amount_paid = order.total,
        status = body['status'],
    )
    payment.save()
    order.payment =payment
    order.is_ordered = True
    order.save()
    
    cart_item = CartItem.objects.filter(user=request.user)
    for x in cart_item:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = x.product_id
        order_product.quantity = x.quantity
        order_product.product_price = x.product.price
        order_product.ordered = True
        order_product.save()
        
    CartItem.objects.filter(user=request.user).delete()

    current_site = get_current_site(request)
    mail_subject = "Thank You For Your Order"
    message = render_to_string('orders/order_received_email.html',{
        'user': request.user,
        "order": order

    })
    to_email = request.user.email
    msg = EmailMessage(mail_subject, message, to=[to_email])
    msg.send()
    
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    cart_count = cart_items.count()
    if cart_count <=0 :
        return redirect("category:category_view")
    
    for item in cart_items:
        total += item.product.price * item.quantity
        
    tax_rate = Decimal(0.05)
    tax = (total * tax_rate)
    tax = Decimal("%.2f" %(tax))
    grand_total = tax + total
    
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = user
            data.first_name = form.cleaned_data.get("first_name")
            data.last_name = form.cleaned_data.get("last_name")
            data.email = form.cleaned_data.get("email")
            data.phone_number = form.cleaned_data.get("phone_number")
            data.country = form.cleaned_data.get("country")
            data.address = form.cleaned_data.get("address")
            data.state = form.cleaned_data.get("state")
            data.city = form.cleaned_data.get("city")
            data.tax = tax
            data.total = grand_total
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'grand_total': grand_total,
                'tax': tax,
                'total': total,
                'cart_items': cart_items
                
            }
            return render(request, 'orders/place_order.html', context)
            
    else:
        return redirect("cart:checkout")    
            
def myorder_view(request):
    qs = OrderProduct.objects.filter(user=request.user, ordered=True)
    
    context = {
        'qs': qs
    }
    return render(request, 'orders/my_order.html', context)


def order_download(request, order_id=None, *args, **kwargs):
    if order_id == None:
        return redirect("order:success")
    qs = OrderProduct.objects.filter(id=order_id, user=request.user, product__media__isnull=False, ordered=True)
    
    order_obj = qs.first()
    product_obj = order_obj.product
    if not product_obj.media:
        return redirect("order:success")
    media = product_obj.media
    product_path = media.path
    path = pathlib.Path(product_path)
    pk = product_obj.pk
    ext = path.suffix
    fname = f"{product_obj}-{pk}{ext}"
    with open(path, 'rb') as f:
        wrapper = FileWrapper(f)
        content_type = 'application/force-download'
        guess_ = guess_type(path)[0]
        
        if guess_:
            content_type = guess_
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={fname}'
        response['X-sendFile'] = f'{fname}'
        return response
    