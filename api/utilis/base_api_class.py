from rest_framework.views import APIView
from rest_framework.response import Response
from .custom_responses import lang_not_found
from rest_framework import status


class CustomBaseApi(APIView):
    def method_not_found_response(self):
        data = {
            "status": False,
            "error": "Method not found or not given!"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def initial(self, request, *args, **kwargs):
        params = request.query_params
        method = params.get("method")
        lang = params.get("lang", "uz")
        if not method:
            return self.method_not_found_response()
        
        if lang not in ['uz', 'ru']:
            return self.lang_not_found_response()

        return None
    

    def lang_not_found_response(self):
        return Response(lang_not_found, status=400)
