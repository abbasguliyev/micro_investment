from django.db import models

class Notification(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pk',)