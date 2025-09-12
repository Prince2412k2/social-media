from django.urls import path

from .views.auth_view import CustomTokenObtainPairView, CustomTokenRefreshView


from .views.user_view import create_user, get_users
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("users/", get_users, name="get-users"),
    path("user/<int:pk>/", get_users, name="get-users"),
    path("signup/", create_user),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
