from django.db import transaction
from notification.models import Notification
from notification.api.selectors import notification_list
from notification.tasks import notification_all_read_task
def notification_create(
        *, user,
        message: str,
        is_read: bool = False
) -> Notification:
    notification = Notification.objects.create(
        user=user,
        message=message,
        is_read=False
    )
    notification.full_clean()
    notification.save()

    return notification


def notification_update(instance, **data) -> Notification:
    notification = notification_list().filter(pk=instance.id).update(**data)
    return notification

def notification_all_read(user) -> bool:
    transaction.on_commit(lambda: notification_all_read_task.delay(user.id))
    return True