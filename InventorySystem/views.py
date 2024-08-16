from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Sale, Inventory, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, SaleSerializer, InventorySerializer, OrderSerializer
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoryFilter, ProductFilter, InventoryFilter

# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter   
    pagination_class = CustomPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    
    