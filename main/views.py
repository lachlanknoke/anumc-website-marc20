"""Views for the ANUMC site."""
from __future__ import annotations

from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from .forms import EventForm, EventSignupForm, UserRegistrationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event: Event = self.get_object()
        user = self.request.user
        # Determine if the current user can view sign‑ups: the event creator or staff
        if user.is_authenticated and (user == event.created_by or user.is_staff):
            context["show_signups"] = True
            context["signups"] = event.signups.all()
        else:
            context["show_signups"] = False
            context["signups"] = None
        return context


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

    def form_valid(self, form):
        # Attach the creator to the event before saving
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):  # type: ignore[override]
        """Ensure only authenticated users can access the create view."""
        return super().dispatch(*args, **kwargs)


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
        # Attach the event and user to the sign‑up instance before saving
        event = self.get_event()
        form.instance.event = event
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            # Pre-fill full_name and email if not provided
            if not form.cleaned_data.get("full_name"):
                form.instance.full_name = self.request.user.profile.full_name
            if not form.cleaned_data.get("email"):
                form.instance.email = self.request.user.email
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the event detail page after successful sign‑up
        return reverse("event-detail", kwargs={"slug": self.kwargs["slug"]})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):  # type: ignore[override]
        """Ensure only authenticated users can sign up for trips."""
        return super().dispatch(*args, **kwargs)


class SignUpView(generic.CreateView):
    """Allow new users to create an account.

    Uses a custom form that collects the username, password and additional
    profile information.  After successful registration, the user is logged in
    and redirected to the home page.
    """

    form_class = UserRegistrationForm
    template_name = "main/signup.html"

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically log the user in after registration
        from django.contrib.auth import login
        login(self.request, self.object)
        return response