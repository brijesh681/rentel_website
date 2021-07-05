from .models import *
import django_filters
from django_filters import DateRangeFilter,DateFilter



class ProductFilter(django_filters.FilterSet):
    product_mrp = django_filters.RangeFilter()
    rental_mrp = django_filters.RangeFilter()
    class Meta:
        model = Product
        fields = ['name','rental_mrp','product_mrp','size']