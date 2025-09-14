"""URL patterns for the main ANUMC app."""
from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("events/<slug:slug>/", views.EventDetailView.as_view(), name="event-detail"),
]