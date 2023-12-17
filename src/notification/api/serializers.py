from django.contrib.auth import get_user_model
from rest_framework import serializers
from notification.models import Notification


class NotificationOutSerializer(serializers.ModelSerializer):
    class NotificationUserInlineSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['id', 'first_name', 'last_name']

    user = NotificationUserInlineSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at']

