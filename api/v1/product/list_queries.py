from .models import Category
from .serializer import CategoryUzSerializer, CategoryRuSerializer
from django.core.cache import cache


def get_category_queryset():
    return Category.objects.select_related('parent').filter(parent__isnull=True)

def get_list_categories(lang=None):
    if lang == None or lang =='uz':
        serializer = CategoryUzSerializer(get_category_queryset(), many=True)
        return serializer.data
    serializer = CategoryRuSerializer(get_category_queryset(), many=True)
    return serializer.data

            