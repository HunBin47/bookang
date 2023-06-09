
from django.db import models
from django.urls import reverse
from store.models import Product 
from accounts.models  import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete= models.CASCADE,default=1)
    
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return self.product.product_name