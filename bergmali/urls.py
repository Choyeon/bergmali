from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from content.views import BlogView, TagView, CategoryView

router = routers.DefaultRouter()
router.register(r'blog', BlogView, basename='blog')
router.register(r'tag', TagView, basename='tag')
router.register(r'category', CategoryView, basename='category')
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
