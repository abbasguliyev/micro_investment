from celery import shared_task
from account.models import UserBalance
from account.api.selectors import user_balance_list, user_list
from account.api.services import user_balance_create

@shared_task(name="user_balance_create_task")
def user_balance_create_task(user_id) -> UserBalance:
    user = user_list().filter(pk=user_id).last()
    user_balance = user_balance_list().filter(user=user)
    print(f"{user_balance=}")
    if user_balance.exists() == False:
        user_balance = user_balance_create(user=user)
    
    return user_balance