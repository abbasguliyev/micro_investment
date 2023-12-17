from notification.models import Notification

def notification_create(
        *, user,
        message: str
) -> Notification:
    notification = Notification.objects.create(
        user=user,
        message=message
    )
    notification.full_clean()
    notification.save()

    return notification
