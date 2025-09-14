"""Admin registrations for ANUMC models."""
from __future__ import annotations

from django.contrib import admin
from .models import Announcement, Event, EventSignup


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "display_on_home")
    list_filter = ("display_on_home",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "start_datetime",
        "end_datetime",
        "category",
        "spots_total",
        "spots_available",
        "approval_status",
    )
    list_filter = ("category", "approval_status")


@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ("event", "full_name", "email", "created_at")
    search_fields = ("full_name", "email", "event__title")