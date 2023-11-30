import os
from datetime import timedelta

from django.utils.encoding import escape_uri_path
from django.utils.translation import gettext_lazy as _

from django.db.models import Sum, Min, Max, Q
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.order.models import OrderItem, Order
from apps.product.filters import ProductFilter
from apps.product.models import CatalogModel, CategoryProductModel, ProductModel, SubCategoryProductModel, \
    FavoriteProductModel
from apps.product.serializers import (AddProductCompareSerializer,
                                      AddProductFavoriteSerializer,
                                      CategorySerializer,
                                      ListCatalogSerializer,
                                      ListProductSerializer,
                                      RetrieveProductSerializer,

                                      SubCategoryProductSerializer,
                                      PopularCategoriesSerializer,
                                      GetProductListSerializer, ListFavoriteProductSerializer, CategoryListSerializer,
                                      ProductReviewInfoSerializer, CreateProductSerializer)
from apps.product.services import ServiceProduct
from apps.review.models import ReviewProductModel
from config.settings import LOGGER


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


class ListProductUserNotReviewView(ListAPIView):
    """Получение товаров пользователя на которые он не сделал отзыв"""
    serializer_class = ProductReviewInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_not_review = ProductModel.objects.filter(order_item_product__order__user=user).exclude(
            review_product__user=user).distinct()
        return product_not_review


class ListProductUserReviewView(ListAPIView):
    """Получение товаров пользователя на которые он сделал отзыв"""
    serializer_class = ProductReviewInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_review_user = ProductModel.objects.filter(review_product__user=user,
                                                          order_item_product__order__user=user).distinct()
        return product_review_user


class ListProductView(ListAPIView):
    """Получение всех товаров с возможностью фильтрации"""
    serializer_class = ListProductSerializer
    queryset = ProductModel.objects.all().filter(is_active=True).order_by('id')
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'product_data__manufacturer__name']
    ordering_fields = ['id', 'name', 'article', 'price', 'discount_price', 'rating', 'date_create', 'product_data',
                       'subcategory']

    def get(self, request, *args, **kwargs):
        """Получение параметров пагинации из query_params)"""
        if page_size := self.request.query_params.get('page_size', None):
            self.pagination_class.page_size = int(page_size)
        return super().get(request, *args, **kwargs)


class MinMaxPriceProduct(APIView):

    def get(self, request, *args, **kwargs):
        """Получение максимальной и минимально цены товаров в зависимости от query_params"""
        query_params = self.request.query_params
        query_clear = {k: v for k, v in query_params.items() if v}
        queryset = ProductModel.objects.select_related('product_data').filter(**query_clear)
        if not queryset:
            min_max_prices = ProductModel.objects.select_related('product_data').all().aggregate(min_price=Min(
                'price'), max_price=Max('price'))
        else:
            min_max_prices = queryset.aggregate(min_price=Min('price'), max_price=Max('price'))
        min_price = min_max_prices['min_price']
        max_price = min_max_prices['max_price']
        return Response({"min_price": min_price, "max_price": max_price})


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
    serializer_class = CategorySerializer

    def get_queryset(self):
        catalog_id = self.kwargs.get('catalog_id')
        return CategoryProductModel.objects.filter(catalog_id=catalog_id).all()


class ListCategoryView(ListAPIView):
    """Получение всех категорий"""
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return CategoryProductModel.objects.all()


class RetrieveCategoryView(RetrieveAPIView):
    """Получение категории по id и ее подкатегории"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryProductModel.objects.all()


class SubcategoryDownloadView(APIView):
    """Скачивание файла со всеми товарами из подкатегории по id"""

    def get(self, request, subcategory_id):
        document = get_object_or_404(SubCategoryProductModel, pk=subcategory_id)
        if document.file_subcategory:
            response = HttpResponse(document.file_subcategory, content_type='application/octet-stream')
            filename = os.path.basename(document.file_subcategory.name)
            encoded_filename = escape_uri_path(filename)
            response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'
            return response
        else:
            return Response(_('Файл не существует'))


class AddProductCompareView(CreateAPIView):
    """Добавление/удаление товара для сравнения"""
    serializer_class = AddProductCompareSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class AddProductFavoriteView(CreateAPIView):
    """Добавление товара в избранное"""
    serializer_class = AddProductFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        ids = self.request.data.get('id')
        serializer.save(user=user, ids=ids)


class ListFavoriteProductView(ListAPIView):
    """Список избранных товаров пользователя"""
    serializer_class = ListFavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FavoriteProductModel.objects.filter(user=user.id)


class DestroyFavoriteProduct(DestroyAPIView):
    """Удаление товара из избранных"""

    def delete(self, request, *args, **kwargs):
        favorite_product = get_object_or_404(FavoriteProductModel, id=self.kwargs['pk'], user=self.request.user)
        favorite_product.delete()
        return Response({"message": "Товар успешно удален из избранных."})


class ListCompareProductView(ListAPIView):
    """Список товаров для сравнения пользователя"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        compare_product_ids = self.request.session.get('compare', [])
        if len(compare_product_ids) <= 1:
            raise ValueError(_('Необходимо два товара для сравнения'))
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


class PopularCategoriesView(ListAPIView):
    """Список первых 4 популярных категорий"""

    serializer_class = PopularCategoriesSerializer

    def get_queryset(self):
        return CategoryProductModel.objects.order_by('-popularity')[:4]


class ViewedProductsView(APIView):
    """Список первых 20 просмотренных товаров"""

    serializer_class = GetProductListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        viewed_products = serializer.validated_data['product_keys']
        products = ProductModel.objects.filter(id__in=viewed_products)[:20]
        serialized_products = ListProductSerializer(products, many=True).data
        return Response({'products': serialized_products})

    # def post(self, request, *args, **kwargs):
    #     viewed_products = request.data.get('products', [])
    #     products = ProductModel.objects.filter(id__in=viewed_products)[:20]
    #     serializer = ListProductSerializer(products, many=True)
    #     return Response(serializer.data)
    # if viewed_products:
    #     return ProductModel.objects.filter(id__in=viewed_products)[:20]
    # return ProductModel.objects.none()


class SimilarProductsView(APIView):
    """Список похожих товаров"""

    serializer_class = GetProductListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        viewed_products = serializer.validated_data['product_keys']
        if viewed_products:
            first_product = ProductModel.objects.get(id=viewed_products[0])
            similar = ProductModel.objects.filter(subcategory=first_product.subcategory, is_active=True).exclude(
                id=first_product.id)[:20]
            serialized_products = ListProductSerializer(similar, many=True).data
            return Response({'products': serialized_products})
        return Response({'products': []})

    # def get_queryset(self):
    #     viewed_products = self.request.session.get('viewed_products', [])
    #     if viewed_products:
    #         first_product = ProductModel.objects.get(id=viewed_products[0])
    #         return ProductModel.objects.filter(subcategory=first_product.subcategory, is_active=True).exclude(
    #             id=first_product.id)[:20]
    #     return ProductModel.objects.none()


class NewProductView(ListAPIView):
    """Список новых товаров"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        return ProductModel.objects.filter(is_active=True).order_by('-date_create')[:20]




class CreateProductView(CreateAPIView):
    serializer_class = CreateProductSerializer
