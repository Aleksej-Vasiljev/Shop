from django.urls import path

from api.views import (test_api, ProductDetailAPIView, ProductListAPIView,
                       ProductCreateAPIView, set_cookie_example, get_cookie_example, RegisterAPIView, ProtectedView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('test/', test_api),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    path('set-cookie/', set_cookie_example),
    path('get-cookie/', get_cookie_example),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='api_register'),
    # path('logout/', LogoutAPIView.as_view(), name='api_logout'),

    path('protected/', ProtectedView.as_view()),
]