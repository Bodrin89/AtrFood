from rest_framework.generics import ListAPIView
from apps.blog.serializers import BlogSerializer
from apps.blog.models import Blog


class ListBlogsView(ListAPIView):
    """Получение всех блогов"""
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
