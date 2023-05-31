from rest_framework import serializers
from django.core.cache import cache

from .models import Category


class CategoryUzSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(source='title_uz', allow_blank=True, default='')
    description = serializers.CharField(source='description_uz', allow_blank=True, default='')

    class Meta:
        model = Category
        fields = ("id", 'icon', 'icon_svg', 'title', 'description', 'children')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data

    # def get_children(self, obj):
    #     cache_key = f'category_children_{obj.id}'
    #     children = cache.get(cache_key)
    #     if children is None:
    #         print("??????")
    #         children = obj.children.all().prefetch_related('children')
    #         cache.set(cache_key, children)
    #     serializer = self.__class__(children, many=True)
    #     return serializer.data
    

class CategoryRuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(source='title_ru', allow_blank=True, default='')
    description = serializers.CharField(source='description_ru', allow_blank=True, default='')

    class Meta:
        model = Category
        fields = ("id", 'icon', 'icon_svg', 'title', 'description', 'children')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data

