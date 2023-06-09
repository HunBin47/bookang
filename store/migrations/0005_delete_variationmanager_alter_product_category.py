# Generated by Django 4.1.7 on 2023-04-16 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0002_remove_category_category_image"),
        ("orders", "0003_remove_orderproduct_variations"),
        ("store", "0004_alter_product_author_alter_product_category_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="VariationManager",),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="category.category",
            ),
        ),
    ]
