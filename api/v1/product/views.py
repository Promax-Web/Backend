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
from .serializer import ProductSerializer
from ...utilis.paginator import Paginator


class CategoryView(CustomBaseApi):
    def get(self, request):
        request_data = request.data
        user = request.user
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

    def get(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        match method:
            case 'list.product':
                page = int(request.GET.get('page', 1))
                limit = 20  # settings.PER_PAGE
                offset = (page - 1) * limit
                query = Product.objects.all()
                pagination = Paginator(request, page=page, per_page=limit, count=len(query))
                meta = pagination.get_paginated_response()
                query = query[offset:offset+limit]
                return Response({
                    "res": self.serializer_class(query, many=True, context={"lang": lang}).data,
                    'meta': meta
                })
