from django.shortcuts import render
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.product.models import CategoryProductModel, SubCategoryProductModel, ProductModel
from apps.review.serializers import ReviewCreateSerializer


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # category_id = self.kwargs.get('category_id')
        # subcategory_id = self.kwargs.get('subcategory_id')
        product_id = self.kwargs.get('product_id')

        # category = get_object_or_404(CategoryProductModel, id=category_id)
        # subcategory = get_object_or_404(SubCategoryProductModel, id=subcategory_id)
        product = get_object_or_404(ProductModel, id=product_id)

        serializer.save(product=product)

