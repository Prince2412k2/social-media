from django.urls import path
from . import views

urlpatterns = [
    # When a user navigates to the URL assigned to this app (e.g., /home/),
    # Django executes the 'home_view' function.
    path("", views.ws_view, name="ws"),
]
