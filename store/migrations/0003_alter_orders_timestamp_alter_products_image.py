# Generated by Django 4.0.2 on 2022-07-06 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_orders_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 6, 11, 37, 6, 848359)),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(max_length=1024, upload_to='static_root/product/'),
        ),
    ]