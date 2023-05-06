from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import get_object_or_404
# from django.core import serializers
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
import datetime
from carts.models import CartItem
from .models import Order, OrderProduct
from store.models import Product
from .serializers import OrderSerializer
from accounts.models import Account

@csrf_exempt
# def place_order(request):
#     current_user = request.user
    
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         serializer = OrderSerializer(data=data)
#         # serializer.user = current_user
#         # data.order_total = serializer['order_total']
#         # data.save()
#         if serializer.is_valid():
#             # serializer.data['user'] = current_user
#             # serializer.data['order_total'] = data['order_total']
#             print(serializer.data['list_product'])
#             product_list = data["list_product"]
#             for p in product_list:
#                 order_product = OrderProduct() 
#                 slug = p["product_slug"]
#                 stocked_product = get_object_or_404(Product.objects.all(), slug=slug)
#                 try:
#                     stocked_product = get_object_or_404(Product.objects.all(), slug=slug)
#                 except Http404:
#                     return JsonResponse({
#                         "message": "Stocked product with slug {} not found".format(slug)
#                     })
#                 if stocked_product.stock - int(p["quantity"]) > 0:
#                     order_product.order =  serializer[data["order"]]
#                     try:
#                         order_product.product = get_object_or_404(Product.objects.all(), slug=p["product_slug"])
#                     except Http404:
#                         return JsonResponse({
#                         "message": "Ordered product with slug {} not found".format(slug)
#                         })
#                     order_product.quantity = p["quantity"] 
#                     stocked_product.stock = stocked_product.stock - p["quantity"]
#                     stocked_product.save()
#                 else:
#                     return JsonResponse({
#                         "message": "The number of items is not enough to fulfill the order"
#                     })

#             # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime("%Y%m%d")    
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()

#             order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number) 
#             return JsonResponse({
#                 'success': True,
#                 'message': 'Order is made successfully',
#                 'order' : order
#             })
#         else:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Invalid order',
#                 'error': serializer.errors 
#             })
#     else:
#         return JsonResponse({
#             'message': 'Invalid method',
#             'error': request.method
#         })
        #else: return JsonResponse(serializer.errors, status=400)
    # else:
    #     # Return response for invalid request method
    #     return HttpResponseNotAllowed(['POST'])
    


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
def place_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = Account.objects.filter(username=data['username'])
        print(user.username)