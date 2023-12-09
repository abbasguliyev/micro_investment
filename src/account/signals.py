from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from account.tasks import user_balance_create_task

@receiver(post_save, sender=get_user_model())
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        user_id = instance.pk
        transaction.on_commit(lambda: user_balance_create_task.delay(user_id))