from allauth import socialaccount
from dj_rest_auth.registration.views import SocialLoginView
from ..models import Credential, User
from allauth.socialaccount.models import SocialAccount, providers
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def permission_create(self, serializer):
        user = serializer.save(self.request)
        social_account = SocialAccount.objects.get(user=user, provider="google")
        Credential.objects.create(
            user=user, provider="google", provider_id=social_account.uid
        )
