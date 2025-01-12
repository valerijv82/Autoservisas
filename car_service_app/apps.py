from django.apps import AppConfig


class CarServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car_service_app'

    def ready(self):
        from .signals import create_profile, save_profile
