from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from project.users.views import RegisterView, LoginView
from project.products.views import ProductViewSet, TopRatedProductsAPIView
from project.orders.views import OrderViewSet
from project.reviews.views import ReviewViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(title="Smart Marketplace API", default_version="v1"),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"products/(?P<product_pk>[^/.]+)/reviews", ReviewViewSet, basename="product-reviews")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/top-products/", TopRatedProductsAPIView.as_view(), name="top-products"),
    path("api/", include(router.urls)),
    path(r"swagger(<format>\.json|\.yaml)", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]