from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer,FullName,Address
from .serializers import CustomerSerializer

class CustomerView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({"message": "Lấy thông tin người dùng thành công","customers": serializer.data}, status=200) 

class CustomerDetail(APIView):
    def get(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            return Response({"message": "Lấy thông tin người dùng thành công", "customer": serializer.data}, status=200)
        except Customer.DoesNotExist:
            return Response({"message": "Người dùng không tồn tại"}, status=404)
        
class CustomerRegister(APIView):
    def post(self, request):
        customer = request.data
        username = customer.get('username')
        if Customer.objects.filter(username=username).exists():
            return Response({"message": "Tên người dùng đã tồn tại"}, status=400)
                            
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Thêm người dùng thành công", "customer": serializer.data}, status=201)
    
class CustomerLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if Customer.objects.get(username=username, password=password):
            return Response({"message": "Đăng nhập thành công"}, status=200)
        return Response({"message": "Tên người dùng hoặc mật khẩu không đúng"}, status=400)
    
class CustomerUpdate(APIView):
    def put(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách hàng'}, status=400)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật thành công!", "customer": serializer.data}, status=200)
        return Response(serializer.errors, status=400)
    
class CustomerDelete(APIView):
    def delete(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách hàng'}, status=400)
        customer.delete()
        return Response({'message': 'Xóa thành công!'}, status=200)
# Create your views here.
