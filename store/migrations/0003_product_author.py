# Generated by Django 4.1.7 on 2023-04-15 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_product_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="author",
            field=models.CharField(default=None, max_length=50),
        ),
    ]
