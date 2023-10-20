import django_filters
from apps.product.models import ProductModel


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    existence = django_filters.BooleanFilter(field_name='existence')
    article = django_filters.CharFilter(field_name='article', lookup_expr='icontains')
    manufacturer = django_filters.CharFilter(field_name='product_data__manufacturer', lookup_expr='icontains')
    made_in = django_filters.CharFilter(field_name='product_data__made_in', lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='subcategory__category__name', lookup_expr='icontains')

    class Meta:
        model = ProductModel
        fields = [
            'min_price',
            'max_price',
            'name',
            'existence',
            'article',
            'manufacturer',
            'made_in',
            'category_name'
        ]
