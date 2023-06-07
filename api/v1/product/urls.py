from django.urls import path
from .views import ProductApi, CategoryView


urlpatterns = [
    path('', ProductApi.as_view()),
    path('category/', CategoryView.as_view())
]
