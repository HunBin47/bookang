from django.db import models
from django.urls import reverse
from accounts.models import Account
from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    images = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self) -> str:
        return self.product_name
    
class VariationManager(models.Model):
    def version(self):
        return super(VariationManager, self).filter(variation_category='version', is_active=True)
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True)
    review = models.TextField(blank=True, max_length=500)
    rating = models.FloatField()
    ip = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject