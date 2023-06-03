from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ...utilis.format import category_format
from rest_framework.views import APIView
from api.utilis.custom_responses import (
    method_not_found_response,
    lang_not_found,
    exception_error_response
)
from main import start


from .list_queries import get_list_categories

class CategoryView(APIView):

    def get(self, request):
        request_data = request.data
        user = request.user
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang")
        if not method:
            return Response(method_not_found_response())
        if lang not in ['uz', 'ru', None]:
            return Response(lang_not_found) 
        match method:
            case 'list.category':
                try:
                    list_categories = get_list_categories(lang)
                except Exception as e:
                    return Response(exception_error_response(e))
                else:
                    return Response(
                        {
                            'status': True,
                            "data": list_categories
                        }
                    )
            case 'id.category':
                pass

