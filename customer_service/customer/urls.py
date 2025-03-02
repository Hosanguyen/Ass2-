from django.urls import path
from .views import CustomerView, CustomerDetail ,CustomerRegister,CustomerLogin,CustomerUpdate,CustomerDelete

urlpatterns = [
    path('customers/',CustomerView.as_view()),
    path('get/<int:id>/',CustomerDetail.as_view()),
    path('register/',CustomerRegister.as_view()),
    path('login/',CustomerLogin.as_view()),
    path('update/<int:id>/',CustomerUpdate.as_view()),
    path('delete/<int:id>/',CustomerDelete.as_view())
]