#cart_service/cart/urls.py
from django.urls import path
from .views import CartDetailAPIView, AddToCartAPIView, RemoveFromCartAPIView, GetOneCartItemAPIView

urlpatterns = [
    path('list/', CartDetailAPIView.as_view(), name='Cart List'),
    path('add/', AddToCartAPIView.as_view(), name='Add Cart'),
    path('delete/', RemoveFromCartAPIView.as_view(), name = 'Delete One Product'),
    path('get/', GetOneCartItemAPIView.as_view(), name = 'Get One Cart Item'),
]