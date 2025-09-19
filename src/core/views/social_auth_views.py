from core.models import Credential
from core.services.google_auth_service import GoogleAuthService
from core.services.github_auth_service import GihubAuthService
from core.views.base_social_auth_view import BaseSocialAuthView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter


class GoogleAuthView(BaseSocialAuthView):
    adapter_class = GoogleOAuth2Adapter
    auth_service = GoogleAuthService
    provider = Credential.Provider.GOOGLE


class GithubAuthView(BaseSocialAuthView):
    adapter_class = GitHubOAuth2Adapter
    auth_service = GihubAuthService
    provider = Credential.Provider.GITHUB
