from rest_framework import serializers
from apps.blog.models import Blog, BlogImage


class BlogImageSerializer(serializers.ModelSerializer):
    """Получение всех картинок"""
    class Meta:
        model = BlogImage
        fields = ('image', )


class BlogSerializer(serializers.ModelSerializer):
    """Получение всех блогов"""

    images = BlogImageSerializer(many=True, )

    class Meta:
        model = Blog
        fields = ('id', 'theme', 'text', 'images', 'date_created')
