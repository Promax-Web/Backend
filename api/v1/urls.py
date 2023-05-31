from django.urls import path
from .product.views import CategoryView


urlpatterns = [
    path('categories/', CategoryView.as_view()),
]



