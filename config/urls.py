from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('api/v1/', include('cityapl.routers')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('', include('finoitpms.urls')),
    path('superadmin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
