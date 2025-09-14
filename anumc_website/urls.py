"""Root URL configuration for the ANUMC Django project."""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    # Authentication URLs (login, logout, password change/reset)
    path("accounts/", include("django.contrib.auth.urls")),
]