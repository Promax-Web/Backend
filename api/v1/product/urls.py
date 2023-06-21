from django.urls import path
from .views import (
    CategoryView,
    ProductApi,
)


urlpatterns = [
    path("", ProductApi.as_view()),
    path("categories/", CategoryView.as_view()),
]
