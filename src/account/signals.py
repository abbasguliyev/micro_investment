from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from account.tasks import user_balance_create_task
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(post_save, sender=get_user_model())
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        user_id = instance.pk
        transaction.on_commit(lambda: user_balance_create_task.delay(user_id))


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # the below like concatinates your websites reset password url and the reset email token which will be required at a later stage
    email_plaintext_message = f"Şifrənizi yeniləmək üçün zəhmət olmasa linkə daxil olun {instance.request.build_absolute_uri('https://halalekosistem.org/reset-password-confirm/')}{reset_password_token.key}"
    
    """
        this below line is the django default sending email function, 
        takes up some parameter (title(email title), message(email body), from(email sender), to(recipient(s))
    """
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Crediation portal account"),
        # message:
        email_plaintext_message,
        # from:
        "abbasquliyev111@gmail.com",
        # to:
        [reset_password_token.user.email],
        fail_silently=False,
    )
