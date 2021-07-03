from django.conf.urls import include, url

from cityapl.views import api_root

urlpatterns = [
    url(r'^$', api_root, name='api_root'),
    url(r'^', include('cityapl.apps.product.routers')),
    url(r'^', include('cityapl.apps.user_auth.routers')),

]