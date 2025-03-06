from django.urls import path
from.views import CreateOrderAPIView,DeleteOrderAPIView, GetAllOrderAPIView, GetDetailOrderAPIView

urlpatterns = [
    path('add/',CreateOrderAPIView.as_view()),
    path('delete/<int:id>/',DeleteOrderAPIView.as_view()),
    path('all/', GetAllOrderAPIView.as_view()),
    path('detail/<int:id>/', GetDetailOrderAPIView.as_view())
]