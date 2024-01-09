# user/serializers.py
from rest_framework import serializers
from django.http import JsonResponse
from .models import Worker, Client, CustomUser

import cloudinary
import cloudinary.uploader
import cloudinary.api	



# Define the upload preset details
upload_preset_name = "multitach_preset1234"
upload_preset_options = {
    "unsigned": False,
    "folder": "multitach",
    "tags": "my_tags",
    "transformation": [
        {"width": 500, "height": 500, "crop": "fill"},
    ],
    "categorization": "aws_rek_tagging",
    "auto_tagging": 0.9
}




class CustomUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)  # Add a password field
    #image_file = serializers.ImageField(write_only=True, required=False)  # Add a new field for image upload

    class Meta:
        model = CustomUser
        fields = ('id','username', 'email','image_url', 'date_of_birth', 'gender','cnic', 'phone','password')
        # fields = ('id', 'email','image_url', 'image_file', 'date_of_birth', 'gender', 'phone','password')
        # read_only_fields = ('image_field',)
        extra_kwargs = {
            'password': {'write_only': True},  # Set write_only to True only for 'password' field
        }
        
    # Corrected method: make it a part of the class and take self as an argument
    def upload_to_cloudinary(self, file_path):
        try:
            existing_preset = cloudinary.api.upload_preset(upload_preset_name)
        except cloudinary.exceptions.ErrorResponse as e:
            if e.status_code == 404:
                upload_preset = cloudinary.api.create_upload_preset(
                    name=upload_preset_name,
                    settings=upload_preset_options
                )
                if upload_preset.get("name") == upload_preset_name:
                    JsonResponse({"message": "preset was uploaded successfully"})
            else:
                JsonResponse({"message": f"Failed to check/upload preset. {e}"})
        else:
            upload_preset = existing_preset

        result = cloudinary.uploader.upload(file_path, upload_preset=upload_preset)
        return result['secure_url']
        
        
    def create(self, validated_data):
        # image_file = validated_data.pop('image_file', None)
        
        # Remove 'image_file' before calling super().create
        user = CustomUser.objects.create(**validated_data)
        
        # if image_file:
        #     cloudinary_upload_result = self.upload_to_cloudinary(image_file.path)
        #     user.image_url = cloudinary_upload_result

        user.save()
        return user
 
    

    def update(self, instance, validated_data):
        #image_file = validated_data.pop('image_file', None)
        
        # Remove 'image_file' before calling super().update
        instance = super().update(instance, validated_data)
        instance.save()
        return instance



        
        
class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Include the parent user fields
    
    class Meta:
        model = Worker
        fields = '__all__'  # Include all fields in the serializer
        read_only_fields = ('base_rating','task_count')
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  # Remove the password from user_data
        user = CustomUser.objects.create(**user_data)  # Create the user instance
        user.set_password(password)  # Set the password for the user
       
        user.save()  # Save the user instance        
        worker = Worker.objects.create(user=user, **validated_data)  # Create the worker instance
        return worker

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Update Worker fields
        instance.workerLocation = validated_data.get('workerLocation', instance.workerLocation)
        instance.workerType = validated_data.get('workerType', instance.workerType)
        instance.base_rating = validated_data.get('base_rating', instance.base_rating)
        instance.task_count = validated_data.get('task_count', instance.task_count)

        # Update user fields if user_data exists
        if user_data:
            instance.user.image_url = user_data.get('image_url', instance.user.image_url)
            instance.user.date_of_birth = user_data.get('date_of_birth', instance.user.date_of_birth)
            instance.user.gender = user_data.get('gender', instance.user.gender)
            instance.user.phone = user_data.get('phone', instance.user.phone)
            instance.user.save()

        instance.save()

        return instance    

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
 
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Update user fields if user_data exists
        if user_data:
            instance.user.image_url = user_data.get('image_url', instance.user.image_url)
            instance.user.date_of_birth = user_data.get('date_of_birth', instance.user.date_of_birth)
            instance.user.gender = user_data.get('gender', instance.user.gender)
            instance.user.phone = user_data.get('phone', instance.user.phone)
            instance.user.save()

        instance.save()

        return instance    

        


