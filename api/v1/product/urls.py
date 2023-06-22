from django.urls import path
from .views import ProductApi, CategoryView


urlpatterns = [
    path("", ProductApi.as_view()),
    path("categories/", CategoryView.as_view()),
]
