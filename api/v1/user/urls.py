from django.urls import path

from .views import *
from ..product.views import CategoryView

urlpatterns = [
    path('auth/', AuthView.as_view()),
    path('category/', CategoryView.as_view())
]