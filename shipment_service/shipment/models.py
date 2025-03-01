from django.db import models
import uuid

class ShippingProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    contact_info = models.TextField()
    api_key = models.CharField(max_length=100, blank=True, null=True)
    api_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ShippingRate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(ShippingProvider, on_delete=models.CASCADE, related_name='rates')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days_min = models.PositiveIntegerField()
    estimated_days_max = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'code')

    def __str__(self):
        return f"{self.provider.name} - {self.name}"

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"

    def full_address(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}, {self.postal_code}"

class Recipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    weight = models.DecimalField(max_digits=8, decimal_places=2, help_text='Weight in kg')
    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Package {self.id} - {self.weight}kg"

    def volume(self):
        if self.length and self.width and self.height:
            return self.length * self.width * self.height
        return None

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã giao cho đơn vị vận chuyển'),
        ('in_transit', 'Đang vận chuyển'),
        ('delivered', 'Đã giao hàng'),
        ('failed', 'Giao hàng thất bại'),
        ('returned', 'Đã hoàn trả'),
        ('cancelled', 'Đã hủy'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    provider = models.ForeignKey(ShippingProvider, on_delete=models.PROTECT, related_name='shipments')
    shipping_rate = models.ForeignKey(ShippingRate, on_delete=models.PROTECT, related_name='shipments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Liên kết với các model đã tách
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT, related_name='shipments')
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='shipments')
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='shipments')
    
    # Thông tin giá cả
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Thông tin thời gian
    estimated_delivery_date = models.DateField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Ghi chú
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Shipment {self.id} - Order {self.order_id}"

class ShipmentEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-occurred_at']
    
    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status} at {self.occurred_at}"