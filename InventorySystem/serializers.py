from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Sale, Order, Stock
from . import models


class SupplierSerializer(serializers.Serializer):
    class Meta:
        model = models.Supplier
        fields = [
            "id",
            "name",
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            "id",
            "name",
        ]


class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Supplier.objects.all(), source="supplier"
    )
    category = serializers.StringRelatedField()

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        source="category",
    )

    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "category",
            "category_id",
            "supplier",
            "supplier_id",
            "stock",
            "description",
            "price",
            "price_with_tax",
        ]


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = [
            "id",
            "user",
            "product",
            "price",
            "quantity_sold",
            "sales_date",
        ]

    def validate(self, data):

        product = data.get("product")
        quantity_sold = data.get("quantity_sold")

        stock = Stock.objects.filter(product=product).first()

        if not stock:
            raise serializers.ValidationError("this product isn't registered on stock")
        if stock.quantity <= quantity_sold:
            raise serializers.ValidationError("not enough stock available")

        return data

    def create(self, validated_data):
        product = validated_data("product")
        quantity_sold = validated_data("quantity_sold")

        sale = Sale.objects.create(**validated_data)

        stock = Stock.objects.filter(product=product).first()
        if stock:
            stock.quantity -= quantity_sold
            stock.save()

        return sale


class OrderItemSerializer(serializers.ModelSerializer):

    order_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Order.objects.all(), source="order"
    )

    class Meta:
        model = models.OrderItem
        fields = ["order_id", "product", "quantity", "price", "price_with_tax"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Customer.objects.all(), source="customer"
    )

    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "customer_id",
            "status",
            "order_items",
            "delivery_address",
            "payment_method",
            "payment_status",
            "order_date",
            "ordered_quantity",
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    product = Product.objects.all()

    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "product",
            "product_id",
            "quantity",
            "payment_method",
            "delivery_address",
        ]

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")
        total_stock = 0
        if product and quantity:
            stock_items = Stock.objects.filter(product=product)
            total_stock = sum(stock_item.quantity for stock_item in stock_items)

        if quantity <= total_stock:
            raise serializers.ValidationError("not enough stock available")
        return data

    def create(self, validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")

        stock_items = Stock.objects.filter(product=product)
        total_stock = sum(stock_item.quantity for stock_item in stock_items)
        stock = stock_items[-1]
        stock.quantity -= quantity
        stock.save()

        order = Order.objects.create(**validated_data)
        return order


class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = []

    def update(self, instance: models.Order, validated_data):
        instance.status == models.Order.CANCELLD_CHOICE
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = [
            "id",
            "name",
            "email",
        ]


class StockSerializer(serializers.Serializer):
    class Meta:
        model = models.Stock
        fields = [
            (
                "product",
                "quantity",
                "time_stamp",
            )
        ]

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", instance.quantity)

        if new_quantity <= 0:
            raise serializers.ValidationError("Quantity must be in positive number")
        new_quantity += instance.quantity

        instance.save()

        return instance


class Restock(serializers.Serializer):
    class Meta:
        models = models.Stock
        fields = []


class SupplierSerializer(serializers.Serializer):
    class Meta:
        model = models.Supplier
        fields = [
            "id",
            "name",
        ]


class PaymentVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50)

    class Meta:
        model = models.Order
        fields = [
            "token",
        ]
