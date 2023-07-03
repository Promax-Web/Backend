from rest_framework.response import Response
from rest_framework.views import APIView
from api.utilis.base_api_class import CustomBaseApi
from api.utilis.custom_responses import (
    exception_error_response
)
from .models import Product, Coloring
from .serializer import (
    ProductDetailSerializer,
    ProductSerializer,
    CertificateProductSerializer,
    ColoringSerializer
)
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
    serializer_class = ProductSerializer
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
                ).annotate()
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


class CertificateApi(APIView):
    serializer_class = CertificateProductSerializer

    def get(self, request, *args, **kwargs):
        params = request.query_params
        lang = params.get("lang", "uz")
        product = Product.objects.all()
        return Response({
            'status': True,
            'data': CertificateProductSerializer(product, many=True, context={'lang': lang}).data
        })


class ColoringApi(APIView):
    serializer_class = ColoringSerializer

    def get(self, request, *args, **kwargs):
        params = request.query_params
        lang = params.get("lang", "uz")
        coloring = Coloring.objects.all()

        return Response({
            'status': True,
            'data': ColoringSerializer(coloring, many=True, context={'lang': lang}).data
        })
