"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include
from django.views.generic import RedirectView

# default evennia patterns
from evennia.web.urls import urlpatterns

# eventual custom patterns
custom_patterns = [
    url(r'^help/', include('web.help_system.urls', namespace='help_system', app_name='help_system')),
    url(r'^clients/', include('web.client_index.urls', namespace='client_index', app_name='client_index')),
    url(r'^plugins/', include('web.plugin_index.urls', namespace='plugin_index', app_name='plugin_index')),

# resources
    url(r'^plugins/GameServer\_command\_plugin\.zip$',  RedirectView.as_view(url='/media/download/GameServer_command_plugin.zip', permanent=False)),
    url(r'^plugins/plugin\_install\_ss1\.png$',  RedirectView.as_view(url='/media/plugin_install_ss1.png', permanent=False)),
    url(r'^plugins/plugin\_install\_ss2\.png$',  RedirectView.as_view(url='/media/plugin_install_ss2.png', permanent=False)),
]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns

