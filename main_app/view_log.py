import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imentor.settings')  # settings.py path
django.setup()

from auditlog.models import LogEntry

for log in LogEntry.objects.all().order_by('-timestamp'):
    print("Model:", log.content_type.model)
    print("Action:", log.get_action_display())
    print("Changes:", log.changes_dict)
    print("User:", log.actor)
    print("Date:", log.timestamp)