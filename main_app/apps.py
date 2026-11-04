
from django.apps import AppConfig
from django.db.utils import OperationalError,ProgrammingError

class MainAppConfig(AppConfig):
    name = 'main_app'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from auditlog.registry import auditlog
        from django.apps import apps

        # Register all models in main_app
        for model in apps.get_app_config('main_app').get_models():
            auditlog.register(model)
            
class MainAppConfig(AppConfig):
    name = "main_app"

    def ready(self):
        """Automatically create the hardcoded dashboard user after migrations."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            User.objects.create_dashboard_user()
        except (OperationalError, ProgrammingError):
            # Happens during the very first migration when the table doesn't exist yet
            pass