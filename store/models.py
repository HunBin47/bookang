from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
from accounts.models import Account
from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    images = CloudinaryField(default=None, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL,related_name="category")
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self) -> str:
        return self.product_name
    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/dy7he6gby/{self.images}"
        )
    
