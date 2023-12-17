from django.db.models.query import QuerySet
from notification.models import Notification

def notification_list() -> QuerySet[Notification]:
    qs = Notification.objects.select_related('user').order_by("-pk").all()
    return qs
