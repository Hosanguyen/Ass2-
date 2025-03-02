from django.db import models

# Create your models here.

class FullName(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'fullname'

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    # zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}"

    class Meta:
        db_table = 'address'

class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('registered', 'Registered Customer'),
        ('guest', 'Guest'),
    ]
    fullname = models.OneToOneField(FullName, on_delete=models.CASCADE, null= True, blank = True)  # Liên kết với FullName
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)  # Liên kết với Address
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='registered')

    def __str__(self):
        return self.fullname.__str__()

    class Meta:
        db_table = 'customer'
