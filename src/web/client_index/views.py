from django.shortcuts import render

def index(request):
    """The 'index' view."""
    return render(request, "client_index/index.html")
