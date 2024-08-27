from django.db.models import Q
import django_filters
from .models import Category, Product, Sale, Order
from django_filters import rest_framework as filters


# class CategoryFilter(django_filters.FilterSet):
#     search = django_filters.CharFilter(method="filter_search")

#     class Meta:
#         model = Category
#         fields = ["search"]

#     def filter_search(self, queryset, name, value):
#         keywords = value.splits()
#         query = Q()

#         for keyword in keywords:
#             query |= Q(name__icontains=keyword)
#         return queryset.filter(query)


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact"],
            "price": ["lte", "gte"],
        }


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "name": {"exact"},
        }


# class OrderFilter(filters.FilterSet):
#     class Meta:
#         model = Order
#         fields = {
#             "product": {"exact"}
        # }