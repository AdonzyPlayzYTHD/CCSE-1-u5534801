# Generated by Django 5.1.3 on 2024-12-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_app', '0004_product_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='security_answer',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='security_question',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
