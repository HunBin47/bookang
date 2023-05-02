from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
import datetime
from carts.models import CartItem
from .models import Order, OrderProduct
from store.models import Product
from .serializers import OrderSerializer

@csrf_exempt
def place_order(request):
    current_user = request.user
    
    # cart_items = CartItem.objects.filter(user=current_user)
    # cart_count = cart_items.count()
    # if cart_count <= 0:
    #     return redirect('store')
    
    if request.method == 'POST':
        serializers = OrderSerializer(request.POST)
        if serializers.is_valid():
            data = Order()
            data.user = current_user
            data.order_total = serializers.cleaned_data['order_total']
            data.is_ordered = serializers.cleaned_data['is_ordered']
            data.save()

            product_list = data["list_product"]
            for p in product_list:
                order_product = OrderProduct() 
                slug = p["product_slug"]
                stocked_product = get_object_or_404(Product.objects.all(), slug=slug)
                if stocked_product.stock - p["quantity"] > 0:
                    order_product.order =  data
                    order_product.product = p["product_slug"]
                    order_product.quantity = p["quantity"] 
                else:
                    return JsonResponse({
                        "message": "The number of items is not enough to fulfill the order"
                    })

            
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")    
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'message': 'Order is made',
                'order' : order
            }
            return JsonResponse(context)

        # order = Order()
        # data = json.loads(request.body)
        # user = data.get('user')
        # order_total = data.get('order_total')
        # is_ordered = data.get('is_ordered')

        # yr = int(datetime.date.today().strftime('%Y'))
        # dt = int(datetime.date.today().strftime('%d'))
        # mt = int(datetime.date.today().strftime('%m'))
        # d = datetime.date(yr, mt, dt)
        # current_date = d.strftime("%Y%m%d")    
        # order_number = current_date + str(data.id)

        # product_list = data["list_product"]
        # for p in product_list:
        #     order_product = OrderProduct() 
        #     order_product.order =  order_number