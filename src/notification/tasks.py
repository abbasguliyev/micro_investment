from celery import shared_task
from notification.api.selectors import notification_list
from account.api.selectors import user_list

@shared_task(name="notification_all_read_task")
def notification_all_read_task(user):
    user = user_list().filter(pk=user).last()
    if user:
        notification_list().filter(user=user).update(is_read=True)