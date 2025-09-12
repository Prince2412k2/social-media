from django.urls import path
from .views.auth_view import CustomTokenObtainPairView
from .views.user_view import create_user, get_users
from rest_framework_simplejwt.views import TokenRefreshView

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adpater_class = GoogleOAuth2Adapter


class GithubLogin(SocialLoginView):
    adpater_class = GitHubOAuth2Adapter


urlpatterns = [
    # temp-paths
    path("users/", get_users, name="get-users"),
    path("user/<int:pk>/", get_users, name="get-users"),
    path("signup/", create_user),
    path("auth/password", CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # Oauth2.0
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/github/", GithubLogin.as_view(), name="github_login"),
]
