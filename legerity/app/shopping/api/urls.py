from django.urls import path
from shopping.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart-items', views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('products/', views.ProductListView.as_view(),name='products'),
    path('category/', views.CategoryListView.as_view(),name='category'),
    path('checkout/', views.OrderView.as_view(),name='checkout'),
]

urlpatterns += router.urls