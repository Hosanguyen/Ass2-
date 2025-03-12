#cart_service/cart/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
import requests
from .serializers import CartItemSerializer, CartSerializer
from django.core.exceptions import ObjectDoesNotExist
from dotenv import load_dotenv
import os
load_dotenv()

product_api = os.getenv('product_api')

class AddToCartAPIView(APIView):
    def post(self, request):
        customerId = request.data.get('customerId')
        productId = request.data.get('productId')
        quantity = request.data.get('quantity')

        cart, _ = Cart.objects.get_or_create(user_id=customerId)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=productId)

        if created:
            cart.total_items += 1
            cart_item.quantity = quantity
            cart.save()
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return Response({'message': 'Added to cart'}, status=status.HTTP_201_CREATED)


class CartDetailAPIView(APIView):
    def get(self, request):
        customerId = request.data.get('customerId')
        
        if not customerId:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart = Cart.objects.get(user_id=customerId)
        except ObjectDoesNotExist:
            return Response({"error": 'Cart not found'}, status=status.HTTP_200_OK)

        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return Response({"cart_items": [], "total_price": 0}, status=status.HTTP_200_OK)

        cart_data = []
        total_price = 0

        for item in cart_items:
            try:
                response = requests.get(f"{product_api}get/", json={'productId': str(item.product)})
                
                if response.status_code != 200:
                    continue  

                product = response.json().get('data')
                
                item_data = {
                    'id': item.id,
                    'product': product,
                    'quantity': item.quantity,
                    'total_price': round(item.quantity * product.get('product_price', 0), 2),
                }
                
                cart_data.append(item_data)
                total_price += item_data['total_price']
            
            except requests.RequestException:
                continue  

        return Response({
            'cart_items': cart_data,
            'total_price': round(total_price, 2),
        }, status=status.HTTP_200_OK)

class GetOneCartItemAPIView(APIView):
    def get(self, request):
        customerId = request.data.get('customerId')
        cartItemId = request.data.get('cartItemId')
        
        if not customerId or not cartItemId:
            return Response({"error": "Customer ID and Cart Item ID are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart = Cart.objects.get(user_id=customerId)
        except ObjectDoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, id=cartItemId)
        except ObjectDoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = requests.get(f"{product_api}get/", json={'productId': str(cart_item.product)})
            if response.status_code != 200:
                return Response({"error": "Failed to fetch product details"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            product = response.json().get('data', {})
            item_data = {
                'id': cart_item.id,
                'product': product,
                'quantity': cart_item.quantity,
                'total_price': round(cart_item.quantity * product.get('product_price', 0), 2),
            }
            
            return Response(item_data, status=status.HTTP_200_OK)
        
        except requests.RequestException:
            return Response({"error": "Failed to connect to product API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class RemoveFromCartAPIView(APIView):
    def delete(self, request):
        customerId = request.data.get('customerId')
        cartItemId = request.data.get('cartItemId')
        quantity = request.data.get('quantity') 
        if not customerId or not cartItemId:
            return Response({"error": "customerId and cartItemId are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user_id=customerId)
        except ObjectDoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(id=cartItemId, cart=cart).first()

        if not cart_item:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        if not quantity:
            quantity = cart_item.quantity
            
        cart_item.quantity -= quantity
        if(cart_item.quantity <=0):
            cart_item.delete()
        else:
            cart_item.save()

        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
