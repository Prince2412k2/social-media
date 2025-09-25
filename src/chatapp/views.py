from django.shortcuts import render


def ws_view(request):
    return render(request, "chatapp/index.html", {})
