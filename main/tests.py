"""
Tests for the ANUMC Django application.

These tests use Django's built-in test client to exercise the views
and check that the rendered pages contain expected content.  They
illustrate how to use Test-Driven Development (TDD) when building
a replacement for the existing Drupal site.  Additional tests should
be added for forms, permissions and other business logic.
"""
from __future__ import annotations

from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from .models import Announcement, Event


class HomePageTests(TestCase):
    def setUp(self) -> None:
        # Create a sample announcement
        Announcement.objects.create(title="ANU Sport not working", body="ANU Sport's website is not currently working.")
        # Create two sample events
        today = date.today()
        Event.objects.create(
            title="Sunday arvo kayak",
            slug="sunday-arvo-kayak",
            category="kayaking",
            description="Come join us for a casual arvo paddle!",
            start_date=today + timedelta(days=1),
            end_date=today + timedelta(days=1),
            fitness_required="Suitable for beginners and most fitness levels",
            spots_total=10,
            spots_available=5,
        )
        Event.objects.create(
            title="Climbing trip to Snake Rock",
            slug="climbing-trip-snake-rock",
            category="climbing",
            description="This trip is at full capacity.",
            start_date=today + timedelta(days=2),
            end_date=today + timedelta(days=2),
            fitness_required="Moderate fitness but no prior experience",
            spots_total=20,
            spots_available=0,
        )

    def test_home_page_status_code(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_welcome_message(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Welcome to the ANU Mountaineering Club!")

    def test_home_page_displays_announcements(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertContains(response, "ANU Sport's website is not currently working.")

    def test_home_page_displays_events(self) -> None:
        response = self.client.get(reverse("home"))
        # Both event titles should be present
        self.assertContains(response, "Sunday arvo kayak")
        self.assertContains(response, "Climbing trip to Snake Rock")
        # The first event still has availability
        self.assertContains(response, "5 / 10 spots left")
        # The second event should be marked as full
        self.assertContains(response, "Full")


class EventModelTest(TestCase):
    def test_is_full_property(self) -> None:
        event = Event(
            title="Test Event",
            slug="test-event",
            category="general",
            description="Description",
            start_date=date.today(),
            end_date=date.today(),
            spots_total=3,
            spots_available=0,
        )
        self.assertTrue(event.is_full)
        event.spots_available = 1
        self.assertFalse(event.is_full)


class EventDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(
            title="Week 8 Sausage Sizzle",
            slug="week-8-sausage-sizzle",
            category="social",
            description="We are planning to meet for a sizzle at Fellows Oval.",
            start_date=date.today(),
            end_date=date.today(),
        )

    def test_event_detail_page_displays_event(self) -> None:
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Week 8 Sausage Sizzle")
        self.assertContains(response, "We are planning to meet for a sizzle at Fellows Oval.")