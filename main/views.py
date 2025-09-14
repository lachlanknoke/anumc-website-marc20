"""Views for the ANUMC site."""
from __future__ import annotations

from django.views import generic

from .models import Announcement, Event


class HomePageView(generic.ListView):
    """Render the home page with announcements and upcoming events."""

    template_name = "main/home.html"
    context_object_name = "events"

    def get_queryset(self):
        # show only upcoming events ordered by start_date
        return Event.objects.order_by("start_date")

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