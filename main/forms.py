"""Forms for creating and signing up to trips.

These forms encapsulate the logic needed to collect user input for
creating new events (trips) and allowing visitors to register their
interest in a trip.  Using Django's ModelForm automatically generates
fields based on the underlying model definitions and provides
validation for free.
"""

from __future__ import annotations

from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Event, EventSignup


class EventForm(forms.ModelForm):
    """Form used by trip leaders to create or edit an Event.

    The form includes all fields necessary to replicate the trip
    creation screen from the Drupal site.  Some fields, such as the
    slug, are handled automatically on save.
    """

    class Meta:
        model = Event
        # Explicitly list the fields in the order they should appear on the form.
        fields = [
            "title",
            "description",
            "meeting_datetime",
            "meeting_location",
            "emergency_contact_details",
            "registration_method",
            "trip_capacity",
            "category",
            "trip_location",
            "start_datetime",
            "end_datetime",
            "difficulty_level",
            "estimated_costs",
            "requested_information",
            "include_prior_experience_checkbox",
            "regular_recurring",
            "approval_status",
            "comment",
            "contact_details",
        ]
        widgets = {
            # Use date/time local inputs for meeting and trip start/end
            "meeting_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 6}),
            "comment": forms.Textarea(attrs={"rows": 3}),
            "requested_information": forms.TextInput(),
        }

    def save(self, commit: bool = True) -> Event:
        """Automatically generate a slug from the title if not provided.

        Because the slug field on the Event model is unique, this helper
        ensures that a sensible slug is created by lowercasing the title
        and replacing spaces with hyphens.  Duplicate slugs will raise
        an integrity error when saving if a trip with the same title
        already exists.
        """
        instance = super().save(commit=False)
        # Generate slug only if this is a new instance and no slug has been set.
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class EventSignupForm(forms.ModelForm):
    """Form for users to register their interest in a trip.

    Only collects the participant's name, email and an optional
    experience/notes field.  The corresponding Event is provided via
    the view and is not exposed on the form.
    """

    class Meta:
        model = EventSignup
        fields = ["full_name", "email", "experience"]
        widgets = {
            "experience": forms.Textarea(attrs={"rows": 4}),
        }


class UserRegistrationForm(forms.ModelForm):
    """Form for registering a new user and capturing profile details.

    This form extends the base ModelForm to create a Django ``User`` together
    with its associated ``UserProfile``.  It asks for username and password
    fields along with full name, email and emergency contact.
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=200, required=True, label="Full name")
    emergency_contact = forms.CharField(max_length=200, required=False, label="Emergency contact")

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "emergency_contact"]

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            # Ensure the profile is created and populated via signals
            profile = user.profile  # triggers signal creation
            profile.full_name = self.cleaned_data.get("full_name")
            profile.email = self.cleaned_data.get("email")
            profile.emergency_contact = self.cleaned_data.get("emergency_contact")
            profile.save()
        return user