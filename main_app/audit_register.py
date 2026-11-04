
from django.apps import apps
from auditlog.registry import auditlog

def register_all_models():
    all_models = apps.get_models()
    for model in all_models:
        try:
            auditlog.register(model)
        except Exception as e:
            print(f"Error registering {model}: {e}")

