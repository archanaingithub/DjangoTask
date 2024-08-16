from django.contrib import admin
from InventorySystem import models

# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]

    list_per_page = 10


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
    ]

    list_per_page = 10
    search_fields = ("name",)
    list_displayI_links = ["name"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "description",
    ]
    search_fields = [
        "name",
        "description",
    ]
    list_per_page = 10
    list_display_links = [
        "name",
    ]


@admin.register(models.Sale)
class SalesAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "product",
        "price",
        "sales_date",
    ]

    list_per_page = 10
    list_display_links = ["product", "customer"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "order_status",
    ]

    class OrderItemInLine(admin.TabularInline):
        model = models.OrderItem
        extra = 2

    inlines = [OrderItemInLine]


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "quantity_in_stock",
    ]

    list_per_page = 5
    list_filter = [
        "product",
    ]


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
    ]

    list_per_page = 5
    list_display_links = [
        "name",
        "email",
    ]
    list_filter = [
        "name",
    ]
