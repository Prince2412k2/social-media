class CookieToHeaderMiddleware:
    """
    Convert HTTPOnlyCookie to header for isauthenticated
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get("access_token")
        if access_token and "HTTP_AUTHORIZATION" not in request.META:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        return self.get_response(request)
