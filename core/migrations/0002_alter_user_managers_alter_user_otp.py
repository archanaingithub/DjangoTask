# Generated by Django 5.1 on 2024-08-16 10:13

import core.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.managers.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]