# shipment_service/shipment/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShippingProviderViewSet, ShippingRateViewSet, ShipmentViewSet,
    AddressViewSet, RecipientViewSet, PackageViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
router = DefaultRouter()
router.register(r'providers', ShippingProviderViewSet)
router.register(r'rates', ShippingRateViewSet)
router.register(r'shipments', ShipmentViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'recipients', RecipientViewSet)
router.register(r'packages', PackageViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Shipment API",
        default_version="v1",
        description="API quản lý vận chuyển",
        terms_of_service="https://yourwebsite.com/terms/",
        contact=openapi.Contact(email="DongVK.B21CN232@stu.ptit.edu.vn"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]