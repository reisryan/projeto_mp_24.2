from django.apps import AppConfig


class FeiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feira'

    def ready(self):
        import feira.signals
