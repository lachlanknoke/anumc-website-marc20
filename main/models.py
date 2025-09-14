"""Database models for the ANUMC site."""
from __future__ import annotations

from django.db import models
from django.urls import reverse


class Announcement(models.Model):
    """A short message displayed on the home page."""

    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Announcement text to be displayed")
    display_on_home = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self) -> str:
        return self.title


class Event(models.Model):
    """A club trip or event.

    This model captures basic information about a trip such as the title,
    description, start and end dates, and capacity.  Additional
    fields may be added later (e.g. GPS coordinates, price, skill
    requirements).
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ("climbing", "Climbing"),
            ("kayaking", "Kayaking"),
            ("skiing", "Skiing"),
            ("hiking", "Hiking"),
            ("social", "Social"),
            ("general", "General"),
        ],
        default="general",
        help_text="Category of the event used for styling and filtering.",
    )
    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
        help_text="Optional image illustrating the event.",
    )
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    fitness_required = models.CharField(max_length=200, blank=True)
    experience_required = models.CharField(max_length=200, blank=True)
    spots_total = models.PositiveIntegerField(default=0)
    spots_available = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("event-detail", args=[self.slug])

    @property
    def is_full(self) -> bool:
        return self.spots_available == 0 and self.spots_total > 0