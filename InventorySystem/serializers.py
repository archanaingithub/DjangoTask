from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Sale, Order, Inventory
from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            "id",
            "name",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "quantity",
            "description",
        ]


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = [
            "id",
            "product",
            "price",
            "quantity",
            "sales_date",
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "status",
            "delivery_address",
            "payment_method",
            "payment_status",
            "order_date",
            "ordered_quantity",
        ]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = [
            "id",
            "product",
            "quantity_in_stock",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = [
            "id",
            "name",
            "email",
        ]