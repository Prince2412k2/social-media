from django.urls import path

from core.views.comment_view import CommentView, DeleteCommentView, GetCommenatsView
from core.views.password_auth_view import (
    PasswordLoginView,
    PasswordSignupView,
    TokenRefreshView,
    LogoutView,
)
from core.views.post_view import (
    DeletePostView,
    PostFetchView,
    UnLikePostView,
    LikePostView,
    PostView,
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
    UpdateUserView,
    get_users,
    get_user,
)


urlpatterns = []

# temp-paths
urlpatterns += [
    path("users/", get_users, name="get-users"),
    path("user/me/", get_user, name="get-users"),
    path("user/profile/", UpdateUserView.as_view(), name="get-users"),
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
urlpatterns += [
    path("user/post", PostView.as_view(), name="post"),
    path("user/posts", PostFetchView.as_view(), name="get-posts"),
    path("user/post/del", DeletePostView.as_view(), name="delte-post"),
    path("user/post/like", LikePostView.as_view(), name="like-post"),
    path("user/post/dislike", UnLikePostView.as_view(), name="like-post"),
]
##Comment Crud endpoints
urlpatterns += [
    path("user/post/comments", GetCommenatsView.as_view(), name="add-comment"),
    path("user/post/comment", CommentView.as_view(), name="add-comment"),
    path("user/post/comment/del", DeleteCommentView.as_view(), name="delete-comment"),
    # path("user/post/del", DeletePostView.as_view(), name="delte-post"),
]
