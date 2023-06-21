from rest_framework.response import Response
from rest_framework.views import APIView
from api.utilis.base_api_class import CustomBaseApi
from api.utilis.custom_responses import (
    exception_error_response
)
from .list_queries import get_list_categories, get_list_products


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


class ProductApi(APIView):

    def get(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        match method:
            case 'list.product':
                category = params.get("category")
                return Response({
                    "status": True,
                    "data": get_list_products(lang, category)
                })
        return Response({
            "status": True,
            "data": "Data"
        })
