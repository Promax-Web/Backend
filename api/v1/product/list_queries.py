from .models import Category
from .serializer import CategoryUzSerializer, CategoryRuSerializer
from django.core.cache import cache


def get_category_queryset():
    return Category.objects.select_related('parent').filter(parent__isnull=True)

def get_list_categories(lang=None):
    cache_key = 'category_data'
    category_data = cache.get(cache_key)
    if not category_data:
        category_data = get_category_queryset()
        cache.set(cache_key, category_data)

    if lang == None or lang =='uz':
        serializer = CategoryUzSerializer(category_data, many=True)
        return serializer.data
    serializer = CategoryRuSerializer(category_data, many=True)
    return serializer.data

            