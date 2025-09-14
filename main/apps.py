from __future__ import annotations

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self) -> None:
        # Import signal handlers to ensure user profiles are created automatically
        from . import signals  # noqa: F401
    verbose_name = "ANUMC Main"