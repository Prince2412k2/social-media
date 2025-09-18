from dj_rest_auth.views import LoginView
from django.urls import path, include

from core.auth import (
    GithubLogin,
    GoogleLogin,
)
from core.views.password_auth_view import (
    PasswordLoginView,
    TokenRefreshView,
    LogoutView,
)
from core.views.user_view import get_users, get_user


urlpatterns = [
    # temp-paths
    path("users/", get_users, name="get-users"),
    path("user/me/", get_user, name="get-users"),
    ##AUTH
    path("auth/login", PasswordLoginView.as_view(), name="Password-Login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="cookie-token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/github/", GithubLogin.as_view(), name="github_login"),
]
