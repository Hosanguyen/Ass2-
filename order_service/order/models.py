from django.db import models

# Create your models here.

class Order(models.Model): 
    user_id = models.IntegerField()
    approved = models.BooleanField(default=False)  # Trạng thái duyệt (False = chưa duyệt, True = đã duyệt)
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo đơn hàng

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Số lượng sản phẩm
    product = models.IntegerField()  # ID sản phẩm