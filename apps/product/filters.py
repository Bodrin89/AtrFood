import django_filters
from apps.product.models import ProductModel


class ProductFilter(django_filters.FilterSet):
    """Фильтр поиска в диапазоне цены"""
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = ProductModel
        fields = [
            'subcategory',
            'existence',
            'article',
            'name',
            'product_data__manufacturer',
            'price',
            'subcategory__category',
        ]
