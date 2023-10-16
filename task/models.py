from django.db import models
from user.models import Client, Worker 
#from feedback.models import Feedback

class Address(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return f"Lat: {self.lat}, Long: {self.long}"


# # Create your models here.
# class Task(models.Model):
    
#     STATUS_CHOICES = [
#         ('TaskPost', 'TaskPosted'),
#         ('TaskAccept', 'TaskAccepted'),
#         ('TaskProcessing', 'TaskProcessing'),
#         ('TaskDeclined', 'TaskDeclined'),
#         ('TaskCompleted', 'TaskCompleted'),
#     ]
    
#     client = models.OneToOneField(Client, on_delete=models.CASCADE)
#     worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    
#     title = models.CharField(max_length = 15)
#     description = models.CharField(max_length = 300)
#     time = models.TimeField()
    
#     address = models.OneToOneField(Address, on_delete = models.CASCADE)  # One-to-one relationship with Address model
#     status =  models.CharField(max_length=20, choices = STATUS_CHOICES, default='TaskPosted')
    