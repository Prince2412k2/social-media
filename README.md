# REST API Development & Security

## Goal

- Create robust REST APIs with authentication and security

### What You Need to Learn

- Django REST Framework (DRF) fundamentals
- Serializers and validation
- ViewSets and generic views
- JWT authentication implementation
- API security, permissions, and rate limiting
- API documentation with drf-spectacular

# Project -Social Media API Backend

- Build a complete REST API with:
  - User registration and JWT authentication
  - Social login integration (Google, GitHub)
  - CRUD operations for posts and comments
  - File upload handling
  - API rate limiting and permissions
  - Interactive API documentation

## User endpoints
    "users/" -> get_users 
    "user/me/" -> get_user
    "user/profile/" -> UpdateUserView -> UserService.Update->User

## Auth endpoints
    auth/signup -> PasswordSignupView 
      ↳ PasswordService | UserService | TokenService  -> User 
    auth/login -> PasswordLoginView 
      ↳ PasswordService | UserService | TokenService -> User 
    auth/refresh -> TokenRefreshView
      ↳ PasswordService | TokenService 
    auth/logout/ -> LogoutView
      ↳ TokenService 
    auth/google/ -> GoogleAuthView
      ↳ SocialAuthView -> GoogleAuthService -> Cred | User
    auth/github/ -> GithubAuthView
      ↳ SocialAuthView -> GitHubAuthService -> Cred | User

## followers endpoints
    user/follow" -> FollowUserView
      ↳ FollowService -> User
    user/unfollow" -> UnfollowUserView
      ↳ FollowService -> User
    user/remove" -> RemoveFollower
      ↳ FollowService -> User
    user/followers" -> GetFollowers
      ↳ FollowService -> User
    user/following" -> GetFollowing
      ↳ FollowService -> User

## post endpoints
    user/post" -> PostView
      ↳ PostService -> Post
    user/post/del" -> DeletePostView
      ↳ PostService -> Post
    user/post/like" -> LikePostView
      ↳ PostService -> Post
    user/post/dislike" -> UnLikePostView
      ↳ PostService -> Post
    user/post/del -> DeletePostView
      ↳ CommentService -> Comment
    
## comment endpoints
    user/post/comments -> GetCommenatsView
      ↳ CommentService -> Comment
    user/post/comment -> CommentView
      ↳ CommentService -> Comment
    user/post/comment/del -> DeleteCommentView
      ↳ CommentService -> Comment
