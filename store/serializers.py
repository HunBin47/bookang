from rest_framework import serializers
from store.models import Product
from category.models import Category
from category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        category_name  = serializers.CharField(source='category.category_name')
        fields = ('product_name', 'slug', 'author', 'description', 'price','category',
                           'stock', 'is_available',  'image_url')
        