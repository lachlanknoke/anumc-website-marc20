"""Views for the ANUMC site."""
from __future__ import annotations

from django.urls import reverse
from django.views import generic

from .forms import EventForm, EventSignupForm
from .models import Announcement, Event, EventSignup


class HomePageView(generic.ListView):
    """Render the home page with announcements and upcoming events."""

    template_name = "main/home.html"
    context_object_name = "events"

    def get_queryset(self):
        # Show only upcoming events ordered by their start date/time.  Use
        # ``start_datetime`` rather than the deprecated ``start_date``.
        return Event.objects.order_by("start_datetime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["announcements"] = Announcement.objects.filter(display_on_home=True)
        return context


class EventDetailView(generic.DetailView):
    """Display details of a single event."""

    model = Event
    template_name = "main/event_detail.html"
    context_object_name = "event"

    slug_field = "slug"
    slug_url_kwarg = "slug"


class EventCreateView(generic.CreateView):
    """Allow trip leaders to create a new event (trip).

    This view uses the EventForm defined in forms.py and, upon
    successful creation, redirects to the detail page for the new
    event.  In a future iteration, access control should be added so
    that only authenticated users with appropriate permissions can
    create trips.
    """

    model = Event
    form_class = EventForm
    template_name = "main/event_form.html"

    def get_success_url(self):
        # After saving, redirect to the newly created event's detail page
        return self.object.get_absolute_url()


class EventSignupView(generic.CreateView):
    """Allow visitors to sign up for a specific event.

    The URL must include the slug of the event being registered for.
    The form captures the participant's name, email and experience
    notes.  Upon successful submission, participants are redirected
    back to the event detail page with a success message.
    """

    model = EventSignup
    form_class = EventSignupForm
    template_name = "main/event_signup_form.html"

    def get_event(self) -> Event:
        # Retrieve the event associated with the current request
        return Event.objects.get(slug=self.kwargs["slug"])

    def form_valid(self, form):
        # Attach the event to the sign‑up instance before saving
        form.instance.event = self.get_event()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the event detail page after successful sign‑up
        return reverse("event-detail", kwargs={"slug": self.kwargs["slug"]})