from django.urls import path, include


urlpatterns = [
    path('product/', include('api.v1.product.urls')),

]
