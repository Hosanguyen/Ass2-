from django.urls import path
from.views import CreateOrderAPIView,DeleteOrderAPIView

urlpatterns = [
    path('add/',CreateOrderAPIView.as_view()),
    path('delete/<int:id>/',DeleteOrderAPIView.as_view()),
]