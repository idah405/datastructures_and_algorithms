from django.apps import AppConfig


class handymanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'handyman'

    def ready(self):
        import handyman.signals

