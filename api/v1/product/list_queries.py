from .models import Category
from .serializer import CategorySerializer
from django.core.cache import cache


def get_category_queryset():
    return Category.objects.select_related('parent')


def get_list_categories(lang, category_id):
    if category_id:
        categories = get_category_queryset().filter(parent_id=category_id)
    else:
        categories = get_category_queryset().filter(parent__isnull=True)
    if not categories.exists():
        return []
    serializer = CategorySerializer(categories, many=True, context={'lang': lang})
    return serializer.data

