from django.db import models

from Backend.api.v1.product.models import Product


# Create your models here.


class Order(models.Model):
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.order.phone