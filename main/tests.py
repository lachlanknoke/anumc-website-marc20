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
from .forms import EventForm, EventSignupForm


class HomePageTests(TestCase):
    def setUp(self) -> None:
        # Create a sample announcement
        Announcement.objects.create(title="ANU Sport not working", body="ANU Sport's website is not currently working.")
        # Create two sample events
        from datetime import datetime
        today = date.today()
        Event.objects.create(
            title="Sunday arvo kayak",
            slug="sunday-arvo-kayak",
            category="kayaking",
            description="Come join us for a casual arvo paddle!",
            start_datetime=datetime.combine(today + timedelta(days=1), datetime.min.time()),
            end_datetime=datetime.combine(today + timedelta(days=1), datetime.min.time()),
            fitness_required="Suitable for beginners and most fitness levels",
            spots_total=10,
            spots_available=5,
        )
        Event.objects.create(
            title="Climbing trip to Snake Rock",
            slug="climbing-trip-snake-rock",
            category="climbing",
            description="This trip is at full capacity.",
            start_datetime=datetime.combine(today + timedelta(days=2), datetime.min.time()),
            end_datetime=datetime.combine(today + timedelta(days=2), datetime.min.time()),
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
        from datetime import datetime
        event = Event(
            title="Test Event",
            slug="test-event",
            category="general",
            description="Description",
            start_datetime=datetime.now(),
            end_datetime=datetime.now(),
            spots_total=3,
            spots_available=0,
        )
        self.assertTrue(event.is_full)
        event.spots_available = 1
        self.assertFalse(event.is_full)


class EventDetailViewTest(TestCase):
    def setUp(self) -> None:
        from datetime import datetime
        self.event = Event.objects.create(
            title="Week 8 Sausage Sizzle",
            slug="week-8-sausage-sizzle",
            category="social",
            description="We are planning to meet for a sizzle at Fellows Oval.",
            start_datetime=datetime.now(),
            end_datetime=datetime.now(),
        )

    def test_event_detail_page_displays_event(self) -> None:
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Week 8 Sausage Sizzle")
        self.assertContains(response, "We are planning to meet for a sizzle at Fellows Oval.")


class EventCreateViewTest(TestCase):
    """Tests for the trip creation view."""

    def test_get_create_view_renders_form(self) -> None:
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, 200)
        # Ensure some expected fields are in the response
        self.assertContains(response, "Title")
        self.assertContains(response, "Description")
        self.assertContains(response, "Trip location")

    def test_post_create_view_creates_event(self) -> None:
        from datetime import datetime
        data = {
            "title": "Test Trip",
            "description": "A test trip.",
            "meeting_datetime": "2025-09-15T10:00",
            "meeting_location": "Union Court",
            "emergency_contact_details": "John Doe 0400 000 000",
            "registration_method": "fcfs",
            "trip_capacity": 5,
            "category": "general",
            "trip_location": "Blue Mountains",
            "start_datetime": "2025-09-20T06:00",
            "end_datetime": "2025-09-21T20:00",
            "difficulty_level": "moderate",
            "estimated_costs": "$50 fuel",
            "requested_information": "prior experience",
            "include_prior_experience_checkbox": "on",
            "regular_recurring": "",
            "approval_status": "approved",
            "comment": "",
            "contact_details": "Jane Doe jane@example.com",
        }
        response = self.client.post(reverse("event-create"), data)
        # Should redirect to the newly created event detail page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.get(title="Test Trip")
        self.assertEqual(event.trip_location, "Blue Mountains")


class EventSignupViewTest(TestCase):
    """Tests for signing up to an event."""

    def setUp(self) -> None:
        from datetime import datetime
        self.event = Event.objects.create(
            title="Sample Trip",
            slug="sample-trip",
            category="general",
            description="Just a sample trip.",
            start_datetime=datetime.now(),
            end_datetime=datetime.now(),
            trip_location="Canberra",
        )

    def test_get_signup_form(self) -> None:
        url = reverse("event-signup", kwargs={"slug": self.event.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up for Sample Trip")

    def test_post_signup_form_creates_signup(self) -> None:
        url = reverse("event-signup", kwargs={"slug": self.event.slug})
        data = {
            "full_name": "Alice Example",
            "email": "alice@example.com",
            "experience": "I have hiked before.",
        }
        response = self.client.post(url, data)
        # Expect redirect back to detail page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.event.signups.count(), 1)
        signup = self.event.signups.first()
        self.assertEqual(signup.full_name, "Alice Example")