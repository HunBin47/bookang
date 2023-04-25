# Generated by Django 4.1.7 on 2023-04-25 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("carts", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="cartitem", name="user",),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]