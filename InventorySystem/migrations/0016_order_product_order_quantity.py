# Generated by Django 5.1 on 2024-08-21 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventorySystem', '0015_remove_product_quantity_product_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='InventorySystem.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
