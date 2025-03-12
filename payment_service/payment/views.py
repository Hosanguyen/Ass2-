# payment_service/payment/views.py
from rest_framework import viewsets
from .models import Payment, PaymentMethod
from .serializers import (
    PaymentSerializer, 
    PaymentMethodSerializer,
    DoPaymentSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
import os
import requests
import dotenv

dotenv.load_dotenv()
SHIPMENT_API = os.getenv('shipment_api')

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

# create do payment only have do_payment action
class DoPaymentViewSet(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        payment = Payment.objects.get(order_id=order_id)
        payment.status = 'completed'
        payment.save()
        
        session = requests.Session()
        response = session.post(f'{SHIPMENT_API}/update_payment/', 
                                json={'order_id': order_id, 'payment_status': 'completed'})
        response.raise_for_status()
        serializer = DoPaymentSerializer(payment)
        return Response(serializer.data)