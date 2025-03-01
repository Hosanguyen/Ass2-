from django.urls import path
from .views import AddProductData, GetProductData, GetOneProduct, DeleteProduct

urlpatterns = [
    path('list/', GetProductData.as_view(), name='Product List'),
    path('add/', AddProductData.as_view(), name='Add Product'),
    path('get/', GetOneProduct.as_view(), name = 'Get One Product'),
    path('delete/', DeleteProduct.as_view(), name = 'Delete Product'),
]