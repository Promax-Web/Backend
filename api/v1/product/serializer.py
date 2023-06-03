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

