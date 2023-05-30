from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .models import Category, Product
from .serializer import CategorySerializer
from ...utilis.format import category_format


class CategoryView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                result = category_format(Category.objects.filter(pk=pk).first())
            except:
                result = "bu id da category yo'q"
        if not pk:
            result = [category_format(i) for i in Category.objects.all()]

        return Response({"category": result})

    def put(self, requests, pk, *args, **kwargs):
        data = requests.data
        category = Category.objects.filter(pk=pk).first()
        if not category:
            return Response({'error': 'bu pkda category topilmadi'})
        serializer = self.get_serializer(data=data, instance=category, partial=True)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        return Response(category_format(root))

    def delete(self, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk).delete()
            result = {"resultat": f"categoriya {pk} id o'chirildi"}
        except:
            result = {"resultat": f"{pk}da categoriya topilmadi"}
        return Response(result)
