# Generated by Django 5.1.3 on 2024-12-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_app', '0003_order_estimated_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory',
            field=models.PositiveIntegerField(default=0),
        ),
    ]