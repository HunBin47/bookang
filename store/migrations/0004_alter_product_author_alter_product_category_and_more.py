# Generated by Django 4.1.7 on 2023-04-16 08:51

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0002_remove_category_category_image"),
        ("store", "0003_product_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="author",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="category.category",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="images",
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
        migrations.DeleteModel(name="ReviewRating",),
    ]
