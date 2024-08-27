# Generated by Django 5.1 on 2024-08-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventorySystem', '0008_remove_sale_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='transaction_type',
            field=models.CharField(choices=[('PURCHASED', 'PURCHASED'), ('SOLD', 'SOLD'), ('RESTOCK', 'RESTOCK')], default=False, max_length=10),
        ),
    ]
