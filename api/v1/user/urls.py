from django.urls import path

from .views import *

urlpatterns = [
    path('auth/', AuthView.as_view())
]