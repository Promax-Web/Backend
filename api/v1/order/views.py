from django.shortcuts import render
from rest_framework.views import APIView

from Backend.api.v1.order.models import Order, OrderItem


class OrderView(APIView):
    def post(self, request):
        params = request.query_params
        method = params.get("method")
        phone = params.get('phone')
        first_name = params.get('first_name')
        last_name = params.get('last_name')
        quantity = params.get('quantity')
        product = params.get('product_id')
        match method:
            case 'order':
                orderItem = OrderItem()
                order = Order()
                order.phone = phone
                order.first_name = first_name
                order.last_name = last_name
                orderItem.order = order
                orderItem.quantity = quantity
                orderItem.product = product
                orderItem.save()
                order.save()