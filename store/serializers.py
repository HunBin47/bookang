from rest_framework import serializers
from store.models import Product, VariationManager, ReviewRating

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name', 'slug', 'description', 'price', 'images', 
                  'stock', 'is_available', 'category', 'created_date', 'modified_date')
class VariationManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationManager
        fields = '__all__'
