from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Shipment)
admin.site.register(ShippingProvider)
admin.site.register(ShippingRate)
admin.site.register(Address)
admin.site.register(Recipient)
admin.site.register(Package)
admin.site.register(ShipmentEvent)
