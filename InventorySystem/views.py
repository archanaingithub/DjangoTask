from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Sale, Order, OrderItem, Stock
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SaleSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CancelOrderSerializer,
    CreateOrderSerializer,
    PaymentVerificationSerializer,
)
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoryFilter, ProductFilter
from django.db.models import Prefetch
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ps.payments.khalti import get_khalti_payment_url
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = Order.objects.prefetch_related(
        Prefetch(
            "order_items",
            queryset=OrderItem.objects.all(),
        )
    )
    permission_classes = (IsAuthenticated,)

    # user login conformation(to see if the user exists in the database)
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return CancelOrderSerializer
        return CreateOrderSerializer

    def cancel(self, request, *args, **kwargs):
        # retrive the instance to be cancelled

        instance = self.get_object()  # fetches the order instance with the given p

        serializer = CancelOrderSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "your order has been successfully cancelled!!"},
        )

    @action(methods=["get"], detail=True)
    def get_payment_method(self, pk):
        order = Order.objects.get(pk=pk)
        url = get_khalti_payment_url(order.pk,order.user, order.total_price_with_tax)
        return (url)
    
    # @swagger_auto_schema(methods=["POST"], request_body=PaymentVerificationSerializer)
    # @action(detail=True, methods=["post"])
    # def get_payment_verification(self, request,pk):
    #     order = Order.objects.get(pk=pk)
    #     serializer = PaymentVerificationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    

class SalesViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
