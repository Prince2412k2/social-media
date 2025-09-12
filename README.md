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

# BugReport

--> [!ERROR] : **Refresh token error**
  - refresh-token was throwing error -> no user for given credentials even when if it was valid.
### PROBLEM
  - simplejwt in DRF only works for AbstractUser provided by django
### FIX
  - added `AUTH_USER_MODEL = "core.User"` in settings to define what class we are using as user for jwt-auth tokens to verify
  - added fake properties to User model in core.models to make django think its a abstarctuser
