from .models import Category, Product
from .serializer import CategorySerializer, ProductSerialiser
from django.core.cache import cache
from django.db.models import Q


def get_category_queryset():
    return Category.objects.select_related('parent')


def get_product_queryset():
    return Product.objects.select_related("category")


def get_list_categories(lang, category):
    if category:
        categories = get_category_queryset().filter(
            Q(parent__title_uz=category) | Q(parent__title_ru=category)
        )
    else:
        categories = get_category_queryset().filter(parent__isnull=True)
    if not categories.exists():
        return []
    serializer = CategorySerializer(categories, many=True, context={'lang': lang})
    return serializer.data


def get_list_products(lang, category=None, product_id=None):
    query = get_product_queryset()
    if category:
        query = get_product_queryset().filter(
            Q(category__title_uz=category) | Q(category__title_ru=category)
        )
    elif product_id:
        query = get_product_queryset().filter(id=product_id).first()
    serializer = ProductSerialiser(query, many=True, context={'lang': lang})
    return serializer.data

