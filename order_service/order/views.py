from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
import requests
import os
import dotenv
dotenv.load_dotenv()

class GetAllOrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        orders_data = []
        for order in orders:
            total_price = 0
            total_items = 0
            items_data = []
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                product_id = order_item.product
                total_items += order_item.quantity
                try:
                    res = requests.get(f'http://localhost:1110/api/product/',json={'productId': product_id})
                    if res.status_code == 200:
                        product = res.json().get('data')
                        total_price += product.get('price') * order_item.quantity
                        items_data.append({
                            'id':order_item.id,
                            'product': product,
                            'quantity':order_item.quantity
                        })
                except requests.exceptions.RequestException as e:
                    return Response({'error': 'Không tìm thấy sản phẩm'}, status=500)
                
            orders_data.append({
                'id': order.id,
                'user_id': order.user_id,
                'total_items': total_items,
                'total_price': total_price,
                'approved': order.approved,
                'items': items_data
            })
        return Response({'message':'Lấy thông tin thành công','data':orders_data}, status=200)

class CreateOrderAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        order_data = {
            'user_id': user_id
        }
        Order.objects.create(**order_data)
        order = Order.objects.latest('created_at')
        
        order_items = request.data.get('order_items')
        for order_item in order_items:
            order_item_data = {
                'order': order,
                'product': order_item.get('product'),
                'quantity': order_item.get('quantity')
            }
            try:
                OrderItem.objects.create(**order_item_data)
            except:
                return Response({'message':'Tạo đơn hàng thất bại'}, status=400)
            # if order_item_serializer.is_valid():
            #     order_item_serializer.save()
            # else:
            #     return Response({'message':'Tạo đơn hàng thất bại'}, status=400)
        return Response({'message':'Tạo đơn hàng thành công'}, status=200)
    

class DeleteOrderAPIView(APIView):
    def delete(self, request,id):
        try:
            order = Order.objects.get(id=id)
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                order_item.delete()
            order.delete()
        except:
            return Response({'message':'Xóa đơn hàng thất bại'}, status=400)
        return Response({'message':'Xóa đơn hàng thành công'}, status=200)
                

            
        

# Create your views here.
