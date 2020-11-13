from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from content.models import Blog, Tag, Category
from content.serializers import BlogSerializer, CategorySerializer, TagSerializer


class BlogView(ModelViewSet):
    """
    博客文章相关接口
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CategoryView(ModelViewSet):
    """
    博客文章相关接口
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagView(ModelViewSet):
    """
    博客文章相关接口
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
