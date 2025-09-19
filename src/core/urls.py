from django.urls import path

from core.views.password_auth_view import (
    PasswordLoginView,
    PasswordSignupView,
    TokenRefreshView,
    LogoutView,
)
from core.views.social_auth_views import GoogleAuthView, GithubAuthView
from core.views.follow_view import (
    FollowUserView,
    GetFollowers,
    GetFollowing,
    RemoveFollower,
    UnfollowUserView,
)
from core.views.user_view import (
    get_users,
    get_user,
)


urlpatterns = []

# temp-paths
urlpatterns += [
    path("users/", get_users, name="get-users"),
    path("user/me/", get_user, name="get-users"),
]

# AUTH endpoints
urlpatterns += [
    path("auth/signup/", PasswordSignupView.as_view(), name="password-signup"),
    path("auth/login", PasswordLoginView.as_view(), name="Password-Login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="cookie-token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/google/", GoogleAuthView.as_view(), name="google_login"),
    path("auth/github/", GithubAuthView.as_view(), name="github_login"),
]
##follow crud endpoints
urlpatterns += [
    path("user/follow", FollowUserView, name="follow"),
    path("user/unfollow", UnfollowUserView, name="unfollow"),
    path("user/remove", RemoveFollower, name="remove-follower"),
    path("user/followers", GetFollowers, name="get-followers"),
    path("user/following", GetFollowing, name="get-followers"),
]

##Post Crud endpoints
