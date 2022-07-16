from django.db import models
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from datetime import datetime

# Create your models here.


class Countries(models.Model):
    country = models.CharField(max_length=255, primary_key=True)


class Country_to_state(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)


class Customer_model(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=1023)
    address2 = models.CharField(max_length=1023)
    country = models.ForeignKey(
        Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(
        Country_to_state, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1023)
    brand = models.CharField(max_length=255)
    market_price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField(
        upload_to='media_root/static/product/', max_length=1024)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    description = models.CharField(max_length=102400)
    size_1 = models.BooleanField()
    size_2 = models.BooleanField()
    size_3 = models.BooleanField()
    size_4 = models.BooleanField()
    size_5 = models.BooleanField()
    size_6 = models.BooleanField()
    size_7 = models.BooleanField(default=False)
    size_8 = models.BooleanField(default=False)
    size_9 = models.BooleanField(default=False)
    size_10 = models.BooleanField(default=False)
    size_11 = models.BooleanField(default=False)
    size_12 = models.BooleanField(default=False)
    size_13 = models.BooleanField(default=False)
    size_14 = models.BooleanField(default=False)
    size_15 = models.BooleanField(default=False)
    size_1_quantity = models.IntegerField()
    size_2_quantity = models.IntegerField()
    size_3_quantity = models.IntegerField()
    size_4_quantity = models.IntegerField()
    size_5_quantity = models.IntegerField()
    size_6_quantity = models.IntegerField()
    size_7_quantity = models.IntegerField(default=-1)
    size_8_quantity = models.IntegerField(default=-1)
    size_9_quantity = models.IntegerField(default=-1)
    size_10_quantity = models.IntegerField(default=-1)
    size_11_quantity = models.IntegerField(default=-1)
    size_12_quantity = models.IntegerField(default=-1)
    size_13_quantity = models.IntegerField(default=-1)
    size_14_quantity = models.IntegerField(default=-1)
    size_15_quantity = models.IntegerField(default=-1)
    size_1_quantity_sold = models.IntegerField()
    size_2_quantity_sold = models.IntegerField()
    size_3_quantity_sold = models.IntegerField()
    size_4_quantity_sold = models.IntegerField()
    size_5_quantity_sold = models.IntegerField()
    size_6_quantity_sold = models.IntegerField()
    size_7_quantity_sold = models.IntegerField(default=-1)
    size_8_quantity_sold = models.IntegerField(default=-1)
    size_9_quantity_sold = models.IntegerField(default=-1)
    size_10_quantity_sold = models.IntegerField(default=-1)
    size_11_quantity_sold = models.IntegerField(default=-1)
    size_12_quantity_sold = models.IntegerField(default=-1)
    size_13_quantity_sold = models.IntegerField(default=-1)
    size_14_quantity_sold = models.IntegerField(default=-1)
    size_15_quantity_sold = models.IntegerField(default=-1)
    total_quantity_sold = models.IntegerField(default=0)

    class Meta:
        unique_together = (("brand", "title"),)


class Cart_Items(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (("user_id", "product_id"),)


class Orders(models.Model):
    address_id = models.ForeignKey(Customer_model, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=255)
