"""URL patterns for the main ANUMC app."""
from __future__ import annotations

from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("events/<slug:slug>/", views.EventDetailView.as_view(), name="event-detail"),
    # Trip creation route (regular trip) under the "Organise a Trip!" menu.
    # In a complete implementation this could be restricted by
    # authentication/permissions and extended to support belay courses or
    # social events.  For now it uses a generic slugless path.
    path("organise/regular-trip/", views.EventCreateView.as_view(), name="event-create"),
    # Sign‑up route for a specific event; expects an event slug in the URL.
    path(
        "events/<slug:slug>/signup/",
        views.EventSignupView.as_view(),
        name="event-signup",
    ),
    # Static content pages replicating the Drupal structure.  Each template
    # should be created under templates/main/ and filled with the
    # appropriate HTML content.  These routes preserve readable URLs.
    path("about/benefits/", TemplateView.as_view(template_name="main/benefits.html"), name="benefits"),
    path("about/activities/", TemplateView.as_view(template_name="main/activities.html"), name="activities"),
    path("about/history/", TemplateView.as_view(template_name="main/history.html"), name="history"),
    path("about/ethics/", TemplateView.as_view(template_name="main/ethics.html"), name="ethics"),
    path("gear/location-hours/", TemplateView.as_view(template_name="main/location_hours.html"), name="location-hours"),
    path("gear/rates-rules/", TemplateView.as_view(template_name="main/rates_rules.html"), name="rates-rules"),
    path("contact/faq/", TemplateView.as_view(template_name="main/faq.html"), name="faq"),
    path("contact/signing-up/", TemplateView.as_view(template_name="main/signing_up.html"), name="signing-up"),
    path("contact/member-protection/", TemplateView.as_view(template_name="main/member_protection.html"), name="member-protection"),
    # User registration
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
]