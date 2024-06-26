from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uhtred.base'
    label = 'base'

    def ready(self) -> None:
        from . import signals
