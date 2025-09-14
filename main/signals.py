"""Signals for automatically creating and updating user profiles."""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created: bool, **kwargs: object) -> None:
    """Ensure every user has an associated profile.

    When a new User is created, a corresponding UserProfile is created.  When
    an existing user is saved, the profile is also saved to pick up any
    changes.
    """
    if created:
        UserProfile.objects.create(user=instance, full_name=instance.get_full_name() or instance.username, email=instance.email)
    else:
        # Update the profile email and full name if they changed on the User model
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        profile.full_name = instance.get_full_name() or instance.username
        profile.email = instance.email
        profile.save()