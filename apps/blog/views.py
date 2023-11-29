from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.blog.serializers import BlogSerializer
from apps.blog.models import Blog


class ListBlogsView(ListAPIView):
    """Получение всех блогов"""
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


class GetBlogView(RetrieveAPIView):
    """Получение блога по id"""
    serializer_class = BlogSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Blog.objects.filter(id=pk)


