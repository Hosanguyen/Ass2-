from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    availability = models.CharField(max_length=255)
    product_price = models.FloatField()
    product_description = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name