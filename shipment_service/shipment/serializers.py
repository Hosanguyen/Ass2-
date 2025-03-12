# shipment_service/shipment/serializers.py
from rest_framework import serializers
from .models import (
    ShippingProvider, ShippingRate, Shipment, ShipmentEvent,
    Address, Recipient, Package
)

class ShippingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingProvider
        fields = ['id', 'name', 'code', 'contact_info', 'is_active', 'created_at', 'updated_at']

class ShippingRateSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = ShippingRate
        fields = ['id', 'provider', 'provider_name', 'name', 'code', 'base_price', 
                  'price_per_kg', 'estimated_days_min', 'estimated_days_max', 
                  'is_active', 'created_at', 'updated_at']

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['id', 'street_address', 'city', 'state', 'country', 'postal_code', 'full_address', 'created_at', 'updated_at']

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'name', 'phone', 'email', 'created_at', 'updated_at']

class PackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Package
        fields = ['id', 'weight', 'length', 'width', 'height', 'volume', 'created_at', 'updated_at']

class ShipmentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentEvent
        fields = ['id', 'status', 'location', 'description', 'occurred_at', 'created_at']

class ShipmentSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    shipping_rate_name = serializers.CharField(source='shipping_rate.name', read_only=True)
    events = ShipmentEventSerializer(many=True, read_only=True)
    
    # Các serializer lồng nhau để hiển thị thông tin đầy đủ
    recipient_details = RecipientSerializer(source='recipient', read_only=True)
    shipping_address_details = AddressSerializer(source='shipping_address', read_only=True)
    package_details = PackageSerializer(source='package', read_only=True)
    
    class Meta:
        model = Shipment
        fields = [
            'id', 'order_id', 'tracking_number', 'provider', 'provider_name',
            'shipping_rate', 'shipping_rate_name', 'status',
            'recipient', 'recipient_details',
            'shipping_address', 'shipping_address_details',
            'package', 'package_details',
            'shipping_cost', 'estimated_delivery_date', 'shipped_at', 'delivered_at',
            'created_at', 'updated_at', 'notes', 'events','payment_status'
        ]

class ShipmentCreateSerializer(serializers.ModelSerializer):
    # Cho phép tạo mới hoặc sử dụng lại các model liên quan
    recipient_data = RecipientSerializer(required=False)
    shipping_address_data = AddressSerializer(required=False)
    package_data = PackageSerializer(required=False)
    
    class Meta:
        model = Shipment
        fields = [
            'id', 'order_id', 'tracking_number', 'provider', 'shipping_rate', 'status',
            'recipient', 'recipient_data',
            'shipping_address', 'shipping_address_data',
            'package', 'package_data',
            'shipping_cost', 'estimated_delivery_date', 'notes', 'payment_status'
        ]
    
    def create(self, validated_data):
        # Xử lý recipient
        recipient_data = validated_data.pop('recipient_data', None)
        recipient_id = validated_data.get('recipient', None)
        
        if not recipient_id and recipient_data:
            recipient = Recipient.objects.create(**recipient_data)
            validated_data['recipient'] = recipient
        
        # Xử lý address
        address_data = validated_data.pop('shipping_address_data', None)
        address_id = validated_data.get('shipping_address', None)
        
        if not address_id and address_data:
            address = Address.objects.create(**address_data)
            validated_data['shipping_address'] = address
        
        # Xử lý package
        package_data = validated_data.pop('package_data', None)
        package_id = validated_data.get('package', None)
        
        if not package_id and package_data:
            package = Package.objects.create(**package_data)
            validated_data['package'] = package
        
        # Tạo shipment
        return super().create(validated_data)
    