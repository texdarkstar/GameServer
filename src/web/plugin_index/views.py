from django.shortcuts import render


def index(request):
    """The 'index' view."""
    return render(request, "plugin_index/index.html")

