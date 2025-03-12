# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PaymentMethodViewSet, PaymentViewSet

# router = DefaultRouter()
# router.register(r'payment-methods', PaymentMethodViewSet)
# router.register(r'payments', PaymentViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
# payment_service/payment/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentViewSet, DoPaymentViewSet
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Tạo router cho API
router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
# router.register(r'do-payment', DoPaymentViewSet)

# Cấu hình Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Payment API",
        default_version="v1",
        description="API quản lý thanh toán",
        terms_of_service="https://yourwebsite.com/terms/",
        contact=openapi.Contact(email="support@yourwebsite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('do_payment/', DoPaymentViewSet.as_view()),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
