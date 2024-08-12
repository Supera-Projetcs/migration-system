from django.apps import AppConfig

class ProcessesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "migration_backend.processes"

    def ready(self):
            import migration_backend.processes.signals