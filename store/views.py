from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from carts.views import _cart_id
from django.db.models import Q


from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct

from store.serializers import ProductSerializer
from store.models import Product
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.core.serializers import serialize

parser_classes = [MultiPartParser, FormParser]

class ListProductView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer

    @csrf_exempt
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


# @api_view(['POST'])
# @authentication_classes(TokenAuthentication)
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = request.data
        print(data)
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Create a new Product successful!'
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def product_detail(request,  product_slug=None):
    model = Product
    serializer_class = ProductSerializer

    try:
        print(product_slug)
        print("Hello")
        single_product = Product.objects.get(slug=product_slug)
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
    context = {
    'single_product': single_product,
    'in_cart': in_cart if 'in_cart' in locals() else False,
    'orderproduct': orderproduct
    }
    return JsonResponse(context)

class ProductDetailView(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('product_slug')
        print(product_slug)
        try:
            obj = get_object_or_404(Product.objects.filter( slug=product_slug))
        except Product.DoesNotExist:
            obj = None
        return obj

    def render_to_response(self, context, **response_kwargs):
        product = context['object']
        if product is not None:
            serializer = ProductSerializer(product)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else: 
            return JsonResponse({
                "error" : "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
@csrf_exempt       
def search(request):
    q = request.GET.get('q', '')
    products = []
    if 'q' in request.GET:
        q = request.GET.get('q')
        products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=q) | Q(description__icontains=q))
    product_count = len(products)
    product_list = json.loads(serialize('json', products)) 
    context = {
        'products': product_list,
        'q': q,
        'product_count': product_count
    }
    return JsonResponse(context)