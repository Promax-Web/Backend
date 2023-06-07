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
from .list_queries import get_list_categories
from .models import Product
from .serializer import ProductSerializer, ProductDetailSerializer
from ...utilis.helper import custom_paginator
from ...utilis.paginator import Paginator


class CategoryView(CustomBaseApi):
    def get(self, request):
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        match method:
            case 'list.category':
                category_id = params.get("category_id")
                try:
                    list_categories = get_list_categories(lang, category_id)
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
    serializer_class = ProductSerializer
    detail_serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        page = int(request.GET.get('page', 1))
        category_id = params.get('category_id')
        product_id = params.get('product_id')
        match method:
            case 'list.product':
                query = Product.objects.all()
                pagination_res = custom_paginator(request, query, page)
                return Response({
                    "status": True,
                    "data": self.serializer_class(pagination_res['queryset'], many=True, context={"lang": lang}).data,
                    'meta': pagination_res['meta']
                })

            case 'category.product':
                query = Product.objects.filter(category_id=category_id)
                pagination_res = custom_paginator(request, query, page)

                return Response({
                    "status": True,
                    "data": self.serializer_class(pagination_res['queryset'], many=True, context={"lang": lang}).data,
                    'meta': pagination_res['meta'],
                })
            case 'detail.product':
                product = Product.objects.filter(id=product_id).first()
                return Response({
                    "status": True,
                    "data": self.detail_serializer_class(product, context={"lang": lang}).data,
                })
