from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Avg, Prefetch
from project.products.serializers import ProductSerializer
from project.products.models import Product
from project.users.permissions import IsSellerOrReadOnly

CACHE_TTL = 60 * 5

class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = ProductSerializer
	permission_classes = (IsSellerOrReadOnly,)
	filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
	filterset_fields = ("category__id",)
	search_fields = ("name", "description")
	ordering_fields = ("price", "created_at")

	def get_queryset(self):
		qs = Product.objects.select_related("category", "seller").prefetch_related(Prefetch("category__products")).all()
		return qs

	@method_decorator(cache_page(CACHE_TTL))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class TopRatedProductsAPIView(generics.ListAPIView):
	serializer_class = ProductSerializer
	permission_classes = (permissions.AllowAny,)

	@method_decorator(cache_page(CACHE_TTL))
	def get(self, request, *args, **kwargs):
		qs = Product.objects.select_related("category", "seller").annotate(avg_rating=Avg("review__rating")).order_by("-avg_rating")[:10]
		page = self.paginate_queryset(qs)
		serializer = self.get_serializer(page, many=True)
		return self.get_paginated_response(serializer.data)
