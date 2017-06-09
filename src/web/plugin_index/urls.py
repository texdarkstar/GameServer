from django.conf.urls import url
from web.plugin_index.views import index

urlpatterns = [
    url(r'^$', index, name="index")
]

