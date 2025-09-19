from django.urls import path, include

from core.views.password_auth_view import (
    PasswordLoginView,
    PasswordSignupView,
    TokenRefreshView,
    LogoutView,
)
from core.views.social_auth_views import GoogleAuthView, GithubAuthView
from core.views.user_view import get_users, get_user


urlpatterns = [
    # temp-paths
    path("users/", get_users, name="get-users"),
    path("user/me/", get_user, name="get-users"),
    ##AUTH
    path("auth/signup/", PasswordSignupView.as_view(), name="password-signup"),
    path("auth/login", PasswordLoginView.as_view(), name="Password-Login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="cookie-token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/google/", GoogleAuthView.as_view(), name="google_login"),
    path("auth/github/", GithubAuthView.as_view(), name="github_login"),
]
