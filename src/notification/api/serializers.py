from django.contrib.auth import get_user_model
from rest_framework import serializers
from notification.models import Notification
from notification.api.selectors import notification_list
from account.api.selectors import user_list

class NotificationOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']


class NotificationCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), write_only=True
    )
    class Meta:
        model = Notification
        fields = ['user', 'message']
        extra_kwargs = {
            'user': {'required': True},
            'message': {'required': True}
        }

class NotificationUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), write_only=True
    )
    class Meta:
        model = Notification
        fields = ['user']
        extra_kwargs = {
            'user': {'required': True}
        }