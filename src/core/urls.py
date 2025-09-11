from django.urls import path

from .views.cred_view import credentials
from .views.user_view import create_user, get_users

urlpatterns = [
    path("users/", get_users, name="get-users"),
    path("user/<int:pk>/", get_users, name="get-users"),
    path("signup/", create_user),
    # path("creds/<int:pk>/", credential, name="credential-detail"),
]
