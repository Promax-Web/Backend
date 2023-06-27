from django.urls import path
from .views import ProductApi, CategoryView, CertificateApi, ColoringApi

urlpatterns = [
    path("", ProductApi.as_view()),
    path("categories/", CategoryView.as_view()),
    path('certificate/', CertificateApi.as_view()),
    path('coloring/', ColoringApi.as_view())
]
