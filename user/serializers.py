# user/serializers.py
from rest_framework import serializers
from .models import Worker, Client, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'image_url', 'date_of_birth', 'gender', 'phone','password')
        extra_kwargs = {
            'password': {'write_only': True},  # Set write_only to True only for 'password' field
        }
        
class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Include the parent user fields
    
    class Meta:
        model = Worker
        fields = '__all__'  # Include all fields in the serializer
        read_only_fields = ('base_rating',)
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  # Remove the password from user_data
        user = CustomUser.objects.create(**user_data)  # Create the user instance
        user.set_password(password)  # Set the password for the user
       
        user.save()  # Save the user instance        
        worker = Worker.objects.create(user=user, **validated_data)  # Create the worker instance
        return worker
        

class ClientSerializer(serializers.ModelSerializer):
    
    user = CustomUserSerializer()  # Include the parent user fields
    class Meta:
        model = Client
        fields = '__all__'  # Include all fields in the serializer

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  # Remove the password from user_data
        user = CustomUser.objects.create(**user_data)  # Create the user instance
        user.set_password(password)  # Set the password for the user
        user.save()  # Save the user instance
        client = Client.objects.create(user=user, **validated_data)  # Create the worker instance
        return client        
        
        


