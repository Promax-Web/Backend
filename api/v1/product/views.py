from rest_framework.response import Response
from rest_framework.views import APIView
from api.utilis.base_api_class import CustomBaseApi
from api.utilis.custom_responses import (
    exception_error_response
)
from .list_queries import get_list_categories


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


class ProductApi(CustomBaseApi):

    def get(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
