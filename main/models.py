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
    # Pre-trip meeting fields
    meeting_datetime = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional date/time for a pre-trip meeting to organise gear",
    )
    meeting_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Location for the pre-trip meeting, if any",
    )
    emergency_contact_details = models.CharField(
        max_length=255,
        blank=True,
        help_text="Emergency contact details provided by the leader",
    )
    # Registration method and capacity
    REGISTRATION_METHOD_CHOICES = [
        ("fcfs", "First Come First Served"),
        ("picky", "Trip Leader Picks"),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_METHOD_CHOICES,
        default="fcfs",
        help_text="Determines whether participants are auto-accepted or manually selected",
    )
    trip_capacity = models.IntegerField(
        default=-1,
        help_text="Maximum number of participants for FCFS trips; leave blank or -1 for unlimited or picky trips",
    )
    # Trip location (where the activity occurs)
    trip_location = models.CharField(max_length=200)
    # Start and end date/time of the actual trip
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    # Difficulty level choices
    DIFFICULTY_CHOICES = [
        ("none", "None"),
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard"),
    ]
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="none",
        help_text="Difficulty level to give participants an idea of what's required",
    )
    estimated_costs = models.CharField(
        max_length=100,
        blank=True,
        help_text="Estimated costs for the trip (e.g. $50 fuel)",
    )
    requested_information = models.CharField(
        max_length=200,
        blank=True,
        help_text="Information to request from participants (e.g. prior experience)",
    )
    include_prior_experience_checkbox = models.BooleanField(
        default=True,
        help_text="Include a checkbox asking about prior experience",
    )
    regular_recurring = models.BooleanField(
        default=False,
        help_text="Mark this as a regular recurring series of trips",
    )
    APPROVAL_STATUS_CHOICES = [
        ("approved", "Approved"),
        ("pending", "Pending"),
    ]
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default="pending",
        help_text="Whether the trip has been approved for publication",
    )
    comment = models.TextField(
        blank=True,
        help_text="Comment describing the changes made when editing",
    )
    contact_details = models.CharField(
        max_length=200,
        help_text="Preferred contact details for the trip leader (hidden from non-members)",
    )
    # Legacy fields for backward compatibility
    fitness_required = models.CharField(max_length=200, blank=True)
    experience_required = models.CharField(max_length=200, blank=True)
    spots_total = models.PositiveIntegerField(default=0)
    spots_available = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order upcoming events by their start date/time.  Use the
        # start_datetime field added below instead of the removed
        # ``start_date`` field from earlier iterations.
        ordering = ["start_datetime"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("event-detail", args=[self.slug])

    @property
    @property
    def is_full(self) -> bool:
        """Return True when the event is at capacity.

        An event is considered full when the number of available spots
        reaches zero and a non‑zero total capacity has been defined.
        Trips with unlimited capacity (spots_total=0) are never full.
        """
        return self.spots_available == 0 and self.spots_total > 0


class EventSignup(models.Model):
    """A sign‑up for an event.

    Rather than requiring user accounts for every participant, this simple
    model allows any visitor to register interest in a trip by providing
    their name and contact email.  The ``event`` relation ties the
    sign‑up to a specific Event.  An optional ``experience`` field
    captures prior experience or additional details requested by the
    trip leader.  Duplicate sign‑ups from the same email for the same
    event are prevented via the unique constraint.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="signups")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "email")
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} – {self.event.title}"