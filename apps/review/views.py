from django.shortcuts import render
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.product.models import CategoryProductModel, SubCategoryProductModel, ProductModel
from apps.review.serializers import ReviewCreateSerializer


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    # permission_classes = [IsAuthenticated] # TODO добавить проверку покупал ли пользователь товар

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(product=product)

