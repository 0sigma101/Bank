from django.apps import AppConfig


class FixedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixed'
