from rest_framework import serializers
from carts.models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('cart_id', 'date_created')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('user', 'product', 'cart', 'quantity', 'is_active')