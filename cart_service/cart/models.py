from django.db import models
import uuid

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    total_items = models.IntegerField(default=0)

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product = models.IntegerField()