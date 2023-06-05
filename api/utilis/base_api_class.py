from rest_framework.views import APIView
from rest_framework.response import Response
from .custom_responses import lang_not_found, method_not_found_response


class CustomBaseApi(APIView):
    def initial(self, request, *args, **kwargs):
        params = request.query_params
        method = params.get("method", None)
        lang = params.get("lang", "uz")

        if not method:
            return self.method_not_found_response()
        if lang not in ['uz', 'ru']:
            return self.lang_not_found_response()

        return None

    def method_not_found_response(self):
        return Response(method_not_found_response(), status=400)

    def lang_not_found_response(self):
        return Response(lang_not_found, status=400)
