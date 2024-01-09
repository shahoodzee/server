from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser 
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_worker = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    #field asked by user
    username = models.CharField(max_length=20, null=True)    
    email = models.EmailField(unique=True)
    image_url = models.URLField(null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True) 
    phone = models.CharField(max_length=11, null=True)
    cnic = models.BigIntegerField(null=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
"""Extending Custom User into Worker and Client"""    


class Worker(models.Model):
    
    WORKER_CHOICES = [
        ('Electrician', 'Electrician'),
        ('Plumber', 'Plumber'),
        ('Carpenter', 'Carpenter'),
        ('Goldsmith', 'Goldsmith'),
        ('Blacksmith', 'Blacksmith'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    workerLocation = models.CharField(max_length=30)
    workerType = models.CharField(max_length=20, choices=WORKER_CHOICES)
    base_rating = models.IntegerField(default=1300)
    task_count = models.IntegerField(default =0)
    
    
class Client(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)