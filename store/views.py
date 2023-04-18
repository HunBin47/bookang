from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from carts.views import _cart_id



from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct

from store.serializers import ProductSerializer
from store.models import Product
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

parser_classes = [MultiPartParser, FormParser]
class ListProductView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug is not None:
            categories = get_object_or_404(Category.objects.all(), slug=category_slug)
            queryset = Product.objects.filter(category=categories, is_available=True)
        else:
            queryset = Product.objects.filter(is_available=True).order_by('id')
        return queryset
   

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    
    # def store(self, request, category_slug = None):
    #     if category_slug is not None:
    #         categories = get_object_or_404(Category.objects.all(), category__slug=category_slug)
    #         queryset = Product.objects.all().filter(category = categories, is_available = True)
    #     else:
    #         queryset = Product.objects.all().filter(is_available = True).order_by('id')
    #     return JsonResponse(queryset)
    
# class CreateProductView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer 

class ProductDetailView(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer

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

