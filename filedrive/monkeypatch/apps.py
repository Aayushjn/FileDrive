from django.apps import AppConfig


class MonkeypatchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monkeypatch"

    def ready(self):
        from . import forms  # noqa: F401
        from . import models  # noqa: F401
