from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import get_object_or_404
# from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from carts.models import CartItem, Cart
from .models import Order, OrderProduct
from store.models import Product
# from .serializers import OrderSerializer
from accounts.models import Account

@csrf_exempt
def place_order(request, username):
    if request.method == "POST":
        data = json.loads(request.body)
        order_total = data["order_total"]
        #print(order_total)
        user = Account.objects.filter(username=username).last()
        #print(user.username)
        order = Order.objects.create(user=user)
        carts = Cart.objects.filter(user=user)
        list_items = []
        for cart in carts:
            list_cart_items = CartItem.objects.filter(cart=cart)
            list_items.extend(list_cart_items)
        cart_items = [CartItem(product=item.product, quantity=item.quantity, cart=item.cart) for item in list_items]
        for cart_item in cart_items:
            order_product = OrderProduct() 
            slug = cart_item.product.slug
            stocked_product = get_object_or_404(Product.objects.all(), slug=slug)
            try:
                stocked_product = get_object_or_404(Product.objects.all(), slug=slug)
            except Http404:
                return JsonResponse({
                    'success' : False,
                    "message": "Stocked product with slug {} not found".format(slug)
                })
            if stocked_product.stock - cart_item.quantity > 0:
                order_product.order =  order
                try:
                    order_product.product = get_object_or_404(Product.objects.all(), slug=slug)
                except Http404:
                    return JsonResponse({
                        'success': False,
                        "message": "Ordered product with slug {} not found".format(slug)
                    })
                order_product.quantity = cart_item.quantity 
                stocked_product.stock = stocked_product.stock - cart_item.quantity
                order_product.save()
                stocked_product.save()
            else:
                return JsonResponse({
                    'success': False,
                    "message": "The number of items is not enough to fulfill the order"
                })
        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")    
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.order_total = float(order_total)
        order.save()
        order = Order.objects.get(user=user, order_number=order_number) 
        carts.delete()
        return JsonResponse({
            'success': True,
            'message': 'Order is made successfully',
            # 'order' : order
        })
    else: 
        return JsonResponse({
            'success': False,
            'message': 'Invalid order method',
        })