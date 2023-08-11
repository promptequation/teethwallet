from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'

    def ready(self) -> None:
        import appointment.signals

        if appointment.signals:
            pass
