from django.shortcuts import render
from rest_framework.generics import ListAPIView

from apps.promotion.models import DiscountModel
from apps.promotion.serializers import ListDiscountSerializer


class ListDiscountView(ListAPIView):
    """Список всех акций"""
    queryset = DiscountModel.objects.all()
    serializer_class = ListDiscountSerializer


class ListDiscountIsShowView(ListAPIView):
    """Список всех акций у которых есть картинка и is_show == True"""
    queryset = DiscountModel.objects.filter(is_show=True).exclude(image__exact='')
    serializer_class = ListDiscountSerializer
