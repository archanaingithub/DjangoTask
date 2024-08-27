from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.core.validators import validate_email


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
        return f"{self.name}"


class Customer(ShareModel):
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_full_name(self):
        return self.name

    def get_formatted_email(self):
        return f"Customer_email: [self.email]"

    def clean_email(self):
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError("invalid email address")

    def get_order(self):
        return Order.objects.filter(Customer=self)

    def has_pending_order(self):
        return self.get_order().filter(status="PENDING").exists()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)


class Category(ShareModel):
    name = models.CharField(max_length=22, unique=True)

    def __str__(self):
        return f"{self.name}"


class Product(ShareModel):
    name = models.CharField(max_length=30, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(default=1)
    description = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def price_with_tax(self):
        return (self.price * Decimal(0.13)) + self.price

    def save(self, *args, **kwargs):
        if self.price <= 0:
            raise ValidationError("price must be a positive number")
        super(Product, self).save(*args, **kwargs)

    def adjust_stock(self, quantity):
        if self.stock < quantity:
            raise ValidationError("not enough stock available")
        self.stock += quantity
        self.save()

    def is_in_stock(self, quantity):
        return self.stock >= quantity
    
    


class Sale(ShareModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    sales_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"sale of {self.product}"


class Stock(ShareModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="stocks"
    )
    quantity = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=False)

    def __str__(self) -> str:
        return f"{self.product.name}: {self.quantity} on {self.time_stamp}"


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

    COD_CHOICE = "COD"
    KHALTI_CHOICE = "KHALTI"
    ESEWA_CHOICE = "ESewa"

    PAYMENT_STATUS_CHOICES = [
        (COD_CHOICE, "COD"),
        (KHALTI_CHOICE, "KHALTI"),
        (ESEWA_CHOICE, "ESewa"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES, max_length=20, default=PENDING_CHOICE
    )

    delivery_address = models.CharField(max_length=50)

    payment_method = models.CharField(choices=PAYMENT_STATUS_CHOICES, max_length=20)
    payment_status = models.BooleanField(default=False)

    order_date = models.DateTimeField(auto_now_add=True)
    ordered_quantity = models.IntegerField(null=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self) -> str:
        return f"order_no: {self.pk}"
    
    @property
    def total_price_with_tax(self):
        return self.product.price_with_tax


class OrderItem(ShareModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}"

    @property
    def price_with_tax(self):
        return self.price + (self.price * 0.13)

    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price

        if self.quantity <= 0:
            return ValidationError("quantity cannot be zero")

        super().save(*args, **kwargs)
