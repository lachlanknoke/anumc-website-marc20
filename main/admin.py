"""Admin registrations for ANUMC models."""
from __future__ import annotations

from django.contrib import admin
from .models import Announcement, Event


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "display_on_home")
    list_filter = ("display_on_home",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "start_date", "end_date", "category", "spots_total", "spots_available")
    list_filter = ("category",)