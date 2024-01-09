# user/serializers.py
from rest_framework import serializers
from .models import TaskNotification

class TaskNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskNotification
        fields = '__all__'