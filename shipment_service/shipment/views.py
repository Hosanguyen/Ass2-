# shipment_service/shipment/views.py
import datetime
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .models import (
    ShippingProvider, ShippingRate, Shipment, ShipmentEvent,
    Address, Recipient, Package
)
from .serializers import (
    ShippingProviderSerializer, ShippingRateSerializer,
    ShipmentSerializer, ShipmentEventSerializer,
    AddressSerializer, RecipientSerializer, PackageSerializer,
    ShipmentCreateSerializer
)

class ShippingProviderViewSet(viewsets.ModelViewSet):
    queryset = ShippingProvider.objects.filter(is_active=True)
    serializer_class = ShippingProviderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'code']
    filterset_fields = ['is_active']

class ShippingRateViewSet(viewsets.ModelViewSet):
    queryset = ShippingRate.objects.filter(is_active=True)
    serializer_class = ShippingRateSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'code', 'provider__name']
    filterset_fields = ['provider', 'is_active']

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['street_address', 'city', 'state', 'country', 'postal_code']
    filterset_fields = ['city', 'state', 'country']

class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'phone', 'email']

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['weight']

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['order_id', 'tracking_number', 'recipient__name', 'recipient__phone']
    filterset_fields = ['status', 'provider', 'order_id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ShipmentCreateSerializer
        return ShipmentSerializer
    
    def get_queryset(self):
        queryset = Shipment.objects.all().order_by('-created_at')
        
        # Lọc theo ngày tạo
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        location = request.data.get('location')
        description = request.data.get('description')
        occurred_at = request.data.get('occurred_at', datetime.datetime.now())
        
        if not new_status or new_status not in dict(Shipment.STATUS_CHOICES).keys():
            return Response(
                {'error': 'Invalid status. Please provide a valid status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not description:
            return Response(
                {'error': 'Description is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cập nhật trạng thái shipment
        shipment.status = new_status
        
        # Cập nhật các trường đặc biệt dựa trên trạng thái
        if new_status == 'shipped':
            shipment.shipped_at = occurred_at
        elif new_status == 'delivered':
            shipment.delivered_at = occurred_at
        
        shipment.save()
        
        # Tạo event mới
        event = ShipmentEvent.objects.create(
            shipment=shipment,
            status=new_status,
            location=location,
            description=description,
            occurred_at=occurred_at
        )
        
        # Thông báo cho order service về sự thay đổi trạng thái
        # try:
        #     requests.post(
        #         f"{settings.ORDER_SERVICE_URL}/orders/{shipment.order_id}/shipping-update/",
        #         json={
        #             'shipment_id': str(shipment.id),
        #             'tracking_number': shipment.tracking_number,
        #             'status': new_status,
        #             'description': description,
        #             'occurred_at': occurred_at.isoformat()
        #         }
        #     )
        # except Exception as e:
        #     # Log lỗi nhưng không làm ảnh hưởng đến response
        #     print(f"Error notifying order service: {e}")
        
        return Response(ShipmentEventSerializer(event).data)
    
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        shipment = self.get_object()
        events = shipment.events.all().order_by('-occurred_at')
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = ShipmentEventSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ShipmentEventSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def calculate_shipping(self, request):
        weight = request.query_params.get('weight')
        provider_id = request.query_params.get('provider_id')
        country = request.query_params.get('country')
        
        if not weight:
            return Response(
                {'error': 'Weight is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            weight = float(weight)
        except ValueError:
            return Response(
                {'error': 'Weight must be a number.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = ShippingRate.objects.filter(is_active=True)
        
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        
        # Tính giá vận chuyển cho mỗi shipping rate
        results = []
        for rate in queryset:
            shipping_cost = rate.base_price + (weight * rate.price_per_kg)
            results.append({
                'provider_id': str(rate.provider.id),
                'provider_name': rate.provider.name,
                'rate_id': str(rate.id),
                'rate_name': rate.name,
                'shipping_cost': float(shipping_cost),
                'estimated_days_min': rate.estimated_days_min,
                'estimated_days_max': rate.estimated_days_max
            })
        
        return Response(results)

class Update_Payment_Status(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        payment_status = request.data.get('payment_status')
        shipment = Shipment.objects.get(order_id=order_id)
        shipment.payment_status = payment_status
        shipment.save()
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)