from rest_framework import serializers
from store.models import Product
from category.models import Category
from category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category_name  = serializers.CharField(source='category.category_name',read_only=True)
    class Meta:
        model = Product
        fields = ('product_name', 'slug', 'author', 'description', 'price','category_name',
                           'stock', 'is_available',  'image_url')
        