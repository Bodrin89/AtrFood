from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from apps.order.models import OrderItem
from apps.product.filters import ProductFilter
from apps.product.models import CatalogModel, CategoryProductModel, ProductModel, SubCategoryProductModel
from apps.product.serializers import (AddProductCompareSerializer,
                                      AddProductFavoriteSerializer,
                                      CategorySerializer,
                                      ListCatalogSerializer,
                                      ListProductSerializer,
                                      RetrieveProductSerializer,
                                      SubCategoryProductSerializer)
from apps.product.services import ServiceProduct
from config.settings import LOGGER

# class CreateProductView(CreateAPIView):
#     """Создание товара"""
#     # permission_classes = [IsAdminUser]
#     serializer_class = CreateProductSerializer


class GetProductView(RetrieveAPIView):
    """Получение товара по id"""
    serializer_class = RetrieveProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return ProductModel.objects.filter(id=pk, is_active=True)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        ServiceProduct.add_viewed_products(pk, request)
        return super().get(request, *args, **kwargs)


class ListProductView(ListAPIView):
    """Получение всех товаров с возможностью фильтрации"""
    serializer_class = ListProductSerializer
    queryset = ProductModel.objects.all().filter(is_active=True).order_by('id')
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'product_data__manufacturer__name']
    ordering_fields = [
        'id',
        'name',
        'article',
        'price',
        'discount_price',
        'rating',
        'date_create',
        'product_data',
        'subcategory'
    ]

    def get(self, request, *args, **kwargs):
        """Получение параметров пагинации из query_params)"""
        if page_size := self.request.query_params.get('page_size', None):
            self.pagination_class.page_size = int(page_size)
        return super().get(request, *args, **kwargs)


class ListProductSubcategoryView(ListAPIView):
    """Получение списка всех товаров по подкатегориям (получение похожих товаров)"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        return ProductModel.objects.all().filter(subcategory_id=subcategory_id, is_active=True)


class ListProductCategoryView(ListAPIView):
    """Получение всех товаров в категории"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return ProductModel.objects.all().filter(subcategory__category_id=category_id, is_active=True)


class ListProductCatalogView(ListAPIView):
    """Получение всех товаров в каталоге"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        catalog_id = self.kwargs.get('catalog_id')
        return ProductModel.objects.all().filter(subcategory__category_id__catalog_id=catalog_id, is_active=True)


class ListCatalogView(ListAPIView):
    """Получение всех каталогов"""
    queryset = CatalogModel.objects.all()
    serializer_class = ListCatalogSerializer


class ListSubcategoryView(ListAPIView):
    """Получение всех подкатегорий категории"""
    serializer_class = SubCategoryProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return SubCategoryProductModel.objects.filter(category_id=category_id).all()


class ListCategorySubcategoryView(ListAPIView):
    """Получение всех категорий каталога с подкатегориями категории"""
    serializer_class = SubCategoryProductSerializer

    def get_queryset(self):
        catalog_id = self.kwargs.get('catalog_id')
        return CategoryProductModel.objects.filter(catalog_id=catalog_id).all()


class AddProductFavoriteView(CreateAPIView):
    """Добавление/удаление товара в избранное"""
    serializer_class = AddProductFavoriteSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class AddProductCompareView(CreateAPIView):
    """Добавление/удаление товара для сравнения"""
    serializer_class = AddProductCompareSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class ListFavoriteProductView(ListAPIView):
    """Список избранных товаров пользователя"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        favorite_product_ids = self.request.session.get('favorite', [])
        return ProductModel.objects.filter(id__in=favorite_product_ids)


class ListCompareProductView(ListAPIView):
    """Список товаров для сравнения пользователя"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        compare_product_ids = self.request.session.get('compare', [])
        if len(compare_product_ids) <= 1:
            raise ValueError('Необходимо два товара для сравнения')
        return ProductModel.objects.filter(id__in=compare_product_ids)


class PopularProductsView(ListAPIView):
    """Список первых 20 популярных товаров"""

    serializer_class = ListProductSerializer

    def get_queryset(self):
        three_months_ago = timezone.now() - timedelta(days=40)
        popular_products = (
            OrderItem.objects.filter(order__date_created__gte=three_months_ago)
            .values('product_id')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
            [:20]
        )

        popular_product_ids = [item['product_id'] for item in popular_products]
        return ProductModel.objects.filter(id__in=popular_product_ids)


class ViewedProductsView(ListAPIView):
    """Список первых 20 просмотренных товаров"""

    serializer_class = ListProductSerializer

    def get_queryset(self):
        viewed_products = self.request.session.get('viewed_products', [])
        if viewed_products:
            return ProductModel.objects.filter(id__in=viewed_products)
        return ProductModel.objects.none()


class SimilarProductsView(ListAPIView):
    """Список похожих товаров"""

    serializer_class = ListProductSerializer

    def get_queryset(self):
        viewed_products = self.request.session.get('viewed_products', [])
        if viewed_products:
            first_product = ProductModel.objects.get(id=viewed_products[0])
            return ProductModel.objects.filter(subcategory=first_product.subcategory, is_active=True).exclude(
                id=first_product.id)[:20]
        return ProductModel.objects.none()


class NewProductView(ListAPIView):
    """Список новых товаров"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        return ProductModel.objects.filter(is_active=True).order_by('-date_create')[:20]
