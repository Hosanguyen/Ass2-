#payment_service/payment/serializers.py
from rest_framework import serializers
from .models import Payment, PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
class DoPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']
