from django.conf.urls import url
from web.client_index.views import index

urlpatterns = [
    url(r'^$', index, name="index")
]

