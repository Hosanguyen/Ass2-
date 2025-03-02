from django.contrib import admin
from .models import Customer, FullName, Address
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(FullName)

# Register your models here.
