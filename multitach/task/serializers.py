from rest_framework import serializers
from user.serializers import WorkerSerializer, ClientSerializer
from .models import Address, Task
from user.models import Client, Worker


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        
        address_data = validated_data.pop('address')
        client_id = validated_data.pop('client')
        worker_id = validated_data.pop('worker')

        # Create or update related objects
        address = Address.objects.get(**address_data)

        task = Task.objects.create(address=address, client=client_id, worker=worker_id, **validated_data)
        return task