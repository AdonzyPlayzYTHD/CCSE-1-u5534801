# Generated by Django 5.1.3 on 2024-12-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_app', '0002_remove_order_order_number_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
