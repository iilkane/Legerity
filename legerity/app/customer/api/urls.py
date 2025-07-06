from django.urls import path
from customer.api import views 

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    
]