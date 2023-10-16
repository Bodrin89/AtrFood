from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.product.models import CategoryProductModel, SubCategoryProductModel, ProductModel
from apps.order.models import OrderItem
from apps.review.models import ReviewProductModel
from apps.review.serializers import ReviewCreateSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# class ReviewCreateView(CreateAPIView):
#     serializer_class = ReviewCreateSerializer
#     # permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         product_id = self.kwargs.get('product_id')
#         product = get_object_or_404(ProductModel, id=product_id)
#         serializer.save(product=product)

class ReviewProductViewSet(ModelViewSet):
    """Просмотр всех отзывов и создание отзывов с проверкой на покупку товара"""
    queryset = ReviewProductModel.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        user = request.user
        product = request.data.get('product')

        if not OrderItem.objects.filter(order__user=user, product=product).exists():
            return Response({"error": "Вы не можете оставить отзыв на этот товар, так как не совершали его покупку."},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

