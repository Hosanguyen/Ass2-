# payment_service/payment/views.py
from rest_framework import viewsets
from .models import Payment, PaymentMethod
from .serializers import (
    PaymentSerializer, 
    PaymentMethodSerializer
)
from rest_framework.response import Response
import os
import requests

ORDER_API = os.getenv('ORDER_API')

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    # # create payment based on order_id
    # def create(self, request):
    #     order_id = request.data.get('order_id')
        
    #     # call API to get order info
    #     # order_info = requests.get(f'{ORDER_API}/orders/{order_id}')
    #     # order_info = order_info.json()
        
    #     amount = request.data.get('amount')
    #     payment_method_id = request.data.get('payment_method_id')
    #     customer_id = request.data.get('customer_id')
    #     payment = Payment.objects.create(
    #         order_id=order_id,
    #         amount=amount,
    #         payment_method_id=payment_method_id,
    #         customer_id=customer_id
    #     )
    #     payment.save()
    #     serializer = PaymentSerializer(payment)
    #     return Response(serializer.data)

