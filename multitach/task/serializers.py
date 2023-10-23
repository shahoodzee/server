from rest_framework import serializers
from user.serializers import WorkerSerializer, ClientSerializer
from .models import Address, Task


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    worker = WorkerSerializer()
    client = ClientSerializer()

    class Meta:
        model = Task
        fields = '__all__'