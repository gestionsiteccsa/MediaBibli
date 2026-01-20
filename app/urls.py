"""
URL configuration for MediaBiB project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/v1/", include("accounts.api.urls")),
]
