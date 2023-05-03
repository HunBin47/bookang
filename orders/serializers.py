from rest_framework import serializers
from orders.models import Order, OrderProduct
import json


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'order_total']

    # def create(self, validated_data):
    #         order_products_data = validated_data.pop('order_products')
    #         order = Order.objects.create(**validated_data)
    #         for op_data in order_products_data:
    #             OrderProduct.objects.create(order=order, **op_data)
    #         return order
    # def validate(self, data):
    #         order_products_data = data.get('order_products')
    #         if not order_products_data:
    #             raise serializers.ValidationError("At least one order product is required.")
    #         return data

# class OrderProductSerializer(serializers.models):
#     class Meta:
#         model = Order
#         fields = ['order', 'product', 'quantity']

class LibraryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            return [self.default(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        elif isinstance(obj, OrderProduct):
            return {"title": obj.title, "author": obj.author, "publication_date": obj.publication_date}
        else:
            return super().default(obj)