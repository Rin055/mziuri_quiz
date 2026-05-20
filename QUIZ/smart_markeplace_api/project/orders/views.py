from rest_framework import viewsets, permissions
from project.orders.models import Order
from project.orders.serializers import OrderSerializer
from project.users.permissions import IsCustomer

class OrderViewSet(viewsets.ModelViewSet):
	serializer_class = OrderSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if user.role == "Seller":
			return Order.objects.filter(items__product__seller=user).distinct().select_related("customer")
		return Order.objects.filter(customer=user).select_related("customer")
