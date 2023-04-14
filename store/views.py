from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from carts.views import _cart_id



from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct

from store.serializers import ProductSerializer
from store.models import Product, ReviewRating
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView


class ListCreateProductView(ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    def store(request, category_slug = None):
        if category_slug is not None:
            categories = get_object_or_404(Category.objects.all(), slug=category_slug)
            queryset = Product.objects.all().filter(category = categories, is_available = True)
        else:
            queryset = Product.objects.all().filter(is_available = True).order_by('id')
    

class ProductDetailView(RetrieveAPIView):
    def product_detail(request, category_slug, product_slug=None):
        try:
            single_product = Product.objects.get(slug=category_slug, product_slug=product_slug)
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            in_cart = CartItem.objects.filter(
                cart = cart,
                product = single_product
        ).exists()
        except Exception as e:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
        )
        
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except Exception:
            orderproduct = None

        reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

