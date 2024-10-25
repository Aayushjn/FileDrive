from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("files.urls")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
