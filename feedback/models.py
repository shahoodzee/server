from django.db import models
from user.models import Client, Worker
from task.models import Task

# Create your models here.
class Feedback(models.Model):
    
    Exp_CHOICES = [
        ('Best', 'Best'),
        ('Good', 'Good'),
        ('Satisfied', 'Satisfied'),
        ('Bad', 'Bad'),
        ('Worst', 'Worst'),
    ]
    
    Status_CHOICES = [
        ('Given', 'Given'),
        ('Pending', 'Pending'),
    ]
    
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)    
    
    feedback_to_worker = models.CharField(max_length = 300 , null=True)
    feedback_to_client = models.CharField(max_length = 300, null=True)
    
    worker_feedback_status = models.CharField(max_length = 10, choices=Status_CHOICES, null=True)
    client_feedback_status = models.CharField(max_length = 10, choices=Status_CHOICES, null=True)
    
    task_experience = models.CharField(max_length=10, choices=Exp_CHOICES, null=True, default='Pending') 
    
    
    
    


