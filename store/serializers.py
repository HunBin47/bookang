from rest_framework import serializers
from store.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = fields = ('product_name', 'slug', 'author','description', 'price', 'images', 'stock', 'is_available', 'category', 'created_date', 'modified_date')

