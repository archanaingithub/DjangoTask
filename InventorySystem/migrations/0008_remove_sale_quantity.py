# Generated by Django 5.1 on 2024-08-16 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InventorySystem', '0007_rename_product_quantity_inventory_quantity_in_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
    ]
