from celery import shared_task
from account.api.selectors import user_balance_list, user_list, investor_list
from account.api.services import user_balance_create

@shared_task(name="user_balance_create_task")
def user_balance_create_task(user_id):
    user = user_list().filter(pk=user_id).last()
    investor = investor_list().filter(user=user).last()
    user_balance = user_balance_list().filter(user=investor).exists()
    if user_balance == False:
        user_balance_create(user=user)