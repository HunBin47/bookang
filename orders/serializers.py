from rest_framework import serializers
from orders.models import Order, OrderProduct
import json


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [ 'user', 'order_total', 'is_ordered']


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