from rest_framework import viewsets
from .models import Payment, PaymentMethod
from .serializers import (
    PaymentSerializer, 
    PaymentMethodSerializer
)

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

