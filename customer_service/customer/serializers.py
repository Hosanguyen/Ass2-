from rest_framework import serializers
from .models import FullName, Address, Customer

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    fullname = FullNameSerializer()  # Dùng nested serializer
    address = AddressSerializer()    # Dùng nested serializer

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        """
        Tạo mới Customer cùng với FullName và Address nếu có.
        """
        fullname_data = validated_data.pop('fullname', None)
        address_data = validated_data.pop('address', None)

        fullname = FullName.objects.create(**fullname_data) if fullname_data else None
        address = Address.objects.create(**address_data) if address_data else None

        customer = Customer.objects.create(fullname=fullname, address=address, **validated_data)
        return customer

    def update(self, instance, validated_data):
        """
        Cập nhật Customer cùng với FullName và Address nếu có.
        """
        fullname_data = validated_data.pop('fullname', None)
        address_data = validated_data.pop('address', None)

        if fullname_data and instance.fullname:
            for key, value in fullname_data.items():
                setattr(instance.fullname, key, value)
            instance.fullname.save()

        if address_data and instance.address:
            for key, value in address_data.items():
                setattr(instance.address, key, value)
            instance.address.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
