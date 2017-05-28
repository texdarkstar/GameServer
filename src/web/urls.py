"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include

# default evennia patterns
from evennia.web.urls import urlpatterns

# eventual custom patterns
custom_patterns = [
    url(r'^help/', include('web.help_system.urls', namespace='help_system', app_name='help_system')),
    url(r'^clients/', include('web.client_index.urls', namespace='client_index', app_name='client_index')),
]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns

