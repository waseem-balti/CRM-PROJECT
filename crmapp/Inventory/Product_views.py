from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmapp.models import Product, ProductService
from django.shortcuts import get_object_or_404
from .Product_serializer import ProductSerializer, ProductServiceSerializer
from rest_framework.exceptions import NotFound

class ProductViewset(viewsets.ModelViewSet):  # Changed to ModelViewSet
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # You can add more custom validation here if needed
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
        serializer = self.serializer_class(product)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
        

class ProductServiceViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductServiceSerializer

    def get_queryset(self):
        return ProductService.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            product_service = ProductService.objects.get(pk=pk)
        except ProductService.DoesNotExist:
            raise NotFound("Product Service not found.")
        serializer = self.serializer_class(product_service)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            product_service = ProductService.objects.get(pk=pk)
        except ProductService.DoesNotExist:
            raise NotFound("Product Service not found.")
        serializer = self.serializer_class(product_service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            product_service = ProductService.objects.get(pk=pk)
            product_service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductService.DoesNotExist:
            raise NotFound("Product Service not found.")
