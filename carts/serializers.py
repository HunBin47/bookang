from rest_framework import serializers
from carts.models import Cart, CartItem
from store.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('cart_id', 'date_created')

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    # product = ProductSerializer(read_only=True, source='product_id')
    # product_slug = serializers.SlugRelatedField(source='product', read_only=True, slug_field='slug')
    price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ('product', 'cart', 'quantity', 'is_active', 'price')
    def get_price(self, obj):
        return obj.product.price