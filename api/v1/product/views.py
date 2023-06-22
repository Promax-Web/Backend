from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.views import APIView
from api.utilis.base_api_class import CustomBaseApi
from api.utilis.custom_responses import (
    exception_error_response
)
from .models import Product
from .serializer import ProductDetailSerializer,ProductSerialiser
from ...utilis.helper import custom_paginator
from .list_queries import get_list_categories
from django.db.models import Q


class CategoryView(CustomBaseApi):
    def get(self, request):
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        match method:
            case 'list.category':
                category = params.get("category", None)
                try:
                    list_categories = get_list_categories(lang, category)
                except Exception as e:
                    return Response(exception_error_response(e))
                else:
                    return Response(
                        {
                            'status': True,
                            "data": list_categories
                        }
                    )
        return self.method_not_found_response()


class ProductApi(APIView):

    serializer_class = ProductSerialiser
    detail_serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        page = int(request.GET.get('page', 1))
        category = params.get('category')
        product_id = params.get('product_id')
        match method:
            case 'list.product':
                query = Product.objects.all()
                pagination_res = custom_paginator(request, query, page)
                return Response({
                    "status": True,
                    "data": self.serializer_class(pagination_res['queryset'], many=True, context={"lang": lang}).data,
                    'pagination': pagination_res['meta']
                })

            case 'category.product':
                query = Product.objects.filter(
                    Q(category__subTitle_uz=category) | Q(category__subTitle_ru=category)
                )
                pagination_res = custom_paginator(request, query, page)
                return Response({
                    "status": True,
                    "data": self.serializer_class(pagination_res['queryset'], many=True, context={"lang": lang}).data,
                    'pagination': pagination_res['meta'],
                })
            case 'detail.product':
                product = Product.objects.filter(id=product_id).first()
                return Response({
                    "status": True,
                    "data": self.detail_serializer_class(product, context={"lang": lang}).data,
                })

