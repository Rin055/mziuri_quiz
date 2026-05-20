from rest_framework import viewsets, permissions
from project.reviews.models import Review
from project.reviews.serializers import ReviewSerializer
from project.reviews.permissions import IsOwnerOrReadOnly
from project.products.models import Product
from rest_framework.exceptions import NotFound

class ReviewViewSet(viewsets.ModelViewSet):
	serializer_class = ReviewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

	def get_queryset(self):
		product_pk = self.kwargs.get("product_pk")
		try:
			product = Product.objects.get(pk=product_pk)
		except Product.DoesNotExist:
			raise NotFound("Product not found")
		return Review.objects.filter(product=product).select_related("user", "product")

	def perform_create(self, serializer):
		product_pk = self.kwargs.get("product_pk")
		product = Product.objects.get(pk=product_pk)
		serializer.save(user=self.request.user, product=product)
