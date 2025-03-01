from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class GetProductData(APIView):
    def get(self, request):
        products = Product.objects.all()
        if products.count() > 0: 
            serializer = ProductSerializer(products, many=True)
            return Response({
                "status": "Success",
                "status_code": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "status_code": 400,
                "message": "Data is not available."
            }, status=status.HTTP_400_BAD_REQUEST)

class GetOneProduct(APIView):
    def get(self, request):
        productId = request.data.get('productId')
        product = Product.objects.filter(id = productId).first()
        if product:
            serializer = ProductSerializer(product)
            return Response({
                "status": "Success",
                "status_code": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "status_code": 400,
                "message": "Data is not available."
            }, status=status.HTTP_400_BAD_REQUEST)


class AddProductData(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book added successfully", "book": serializer.data}, status=201)
        return Response(serializer.errors, status=400)

class DeleteProduct(APIView):
    def delete(self, request):
        productId = request.data.get("productId")
        product = Product.objects.filter(id = productId).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'message': 'Product has been deleted'}, status=status.HTTP_200_OK)
