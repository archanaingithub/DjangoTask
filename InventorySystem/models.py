from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.


class ShareModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(ShareModel):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.email}"


class Customer(ShareModel):
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.email}"

class Category(ShareModel):
    name = models.CharField(max_length=22, unique=True)

    def __str__(self):
        return f"{self.name}"


class Product(ShareModel):
    name = models.CharField(max_length=30, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}-{self.price}-{self.description}"
    

class Sale(ShareModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    sales_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"sale of {self.product.name} on {self.sales_date}"
    
    
class Inventory(ShareModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name}-{self.quantity_in_stock} in stock"
    

class Stock(ShareModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=False)
    
    def __str__(self) -> str:
        return f"{self.inventory.product.name}: {self.quantity} on {self.time_stamp}"


class Order(ShareModel):
    PENDING_CHOICE = "PENDING"
    DELIVERED_CHOICE = "DELIVERED"
    CANCELLD_CHOICE = "CANCELLED"
    SHIPPED_CHOICE = "SHIPPED"

    ORDER_STATUS_CHOICES = [
        (PENDING_CHOICE, "PENDING"),
        (DELIVERED_CHOICE, "DELIVERED"),
        (CANCELLD_CHOICE, "CANCELLED"),
        (SHIPPED_CHOICE, "SHIPPED"),
    ]

    CDO_CHOICE = "CDO"
    KHALTI_CHOICE = "KHALTI"
    ESEWA_CHOICE = "ESewa"

    PAYMENT_STATUS_CHOICES = [
        (CDO_CHOICE, "CDO"),
        (KHALTI_CHOICE, "KHALTI"),
        (ESEWA_CHOICE, "ESewa"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        max_length=20,
        default=PENDING_CHOICE)

    delivery_address = models.CharField(max_length=50)

    payment_method = models.CharField(
        choices=PAYMENT_STATUS_CHOICES,
        max_length=20
        )
    payment_status = models.BooleanField(default=False)
    
    order_date = models.DateTimeField(auto_now_add=True)
    ordered_quantity = models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return f"order_no: {self.pk}"


class OrderItem(ShareModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
