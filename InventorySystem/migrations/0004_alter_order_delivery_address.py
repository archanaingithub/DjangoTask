# Generated by Django 5.1 on 2024-08-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventorySystem', '0003_rename_sales_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=50),
        ),
    ]
