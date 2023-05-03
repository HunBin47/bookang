from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from store.models import Product
from carts.models import Cart, CartItem
from accounts.models import Account
from carts.serializers import CartItemSerializer


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

@csrf_exempt
def add_cart(request, product_slug):
    if request.method == 'POST':
        product = Product.objects.get(slug=product_slug)
        if request.user.is_authenticated:
            is_exists_cart_item = CartItem.objects.filter(product=product, cart__user=request.user).exists()
            if is_exists_cart_item:
                cart_items = CartItem.objects.filter(
                    product=product,
                    cart__user=request.user
                )
                # id = [item.id for item in cart_items]
                cart_item = cart_items[0]
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=Cart.objects.create(user=request.user),
                    # cart__user=request.user,
                    quantity=1
                )
            cart_item.save()
            return JsonResponse({
                'message': 'Successfully added'
            })
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()

            is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
            if is_exists_cart_item:
                cart_items = CartItem.objects.filter(
                    product=product,
                    cart=cart
                )
                id = [item.id for item in cart_items]
                cart_item = cart_items[0]
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=1
                )
            cart_item.save()
            return JsonResponse({
                'message': 'Successfully added'
            })
    else:
        return JsonResponse({
            'message': 'Invalid method specified'
        })   

@csrf_exempt
def reduce_cart(request, product_slug):
    if request.method == 'DELETE':
        product = get_object_or_404(Product, slug=product_slug)
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem,
                product=product
            )
        else:
            return JsonResponse({
                'message': 'User is not authenticated'
            })

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse({
            'message': 'Cart item is reduced'
        })
    else: 
        return JsonResponse({
            'message': 'Invalid method'
        })

@csrf_exempt
def remove_cart_item(request, product_slug):
    if request.method == 'DELETE':
        product = get_object_or_404(Product, slug=product_slug)
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem,
                product=product
            )
        else:
            return JsonResponse({
                'message': 'User is not authenticated'
            })
        cart_item.delete()

        return JsonResponse({
            'message': 'Cart item is deleted successfully'
        })
    else: 
        return JsonResponse({
            'message': 'Invalid method'
        })

@csrf_exempt
def cart(request, username):
    if request.method == 'GET':
        try:
            user = Account.objects.get(username=username)
            cart_items = CartItem.objects.filter(cart__user=user, is_active=True)
            serializer = CartItemSerializer(cart_items, many=True)
            cart_items_data = serializer.data
            cart_items_list = [item for item in cart_items_data]
            total = sum([item.get('price') * item['quantity'] for item in cart_items_list])
            quantity = sum([item['quantity'] for item in cart_items_list])
            context = {
                'user': username,
                'total': total,
                'quantity': quantity,
                'cart_items': cart_items_list,
            }
            return JsonResponse(context)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Product not found or user not logged in'})
    else: 
        return JsonResponse({'message': 'Invalid method'})



# @login_required(login_url='login')
# @csrf_exempt
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         #  cart = Cart.objects.get(cart_id=_cart_id(request=request))
#         cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         for cart_item in cart_items:
#             total += cart_item.product.price * cart_item.quantity
#             quantity += cart_item.quantity
#         tax = total * 2 / 100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass    # Chỉ bỏ qua
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax if "tax" in locals() else "",
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context=context)
