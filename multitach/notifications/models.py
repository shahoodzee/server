from django.db import models
from user.models import Client,Worker
from task.models import Task


# Create your models here.
class TaskNotification(models.Model):
    DECISION_CHOICES = [
        ('Accept', 'Accept'),
        ('Reject', 'Reject'),
        ('Pending','Pending'),
    ]
    WORKER_CHOICES = [
        ('Electrician', 'Electrician'),
        ('Plumber', 'Plumber'),
        ('Carpenter', 'Carpenter'),
        ('Goldsmith', 'Goldsmith'),
        ('Blacksmith', 'Blacksmith'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('TaskPost', 'TaskPosted'),
        ('TaskAccept', 'TaskAccepted'),
        ('TaskProcessing', 'TaskProcessing'),
        ('TaskDeclined', 'TaskDeclined'),
        ('TaskCompleted', 'TaskCompleted'),
    ]    
        
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='received_notifications')

    description = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    time = models.TimeField(null=True)
    taskType = models.CharField(max_length=20, choices=WORKER_CHOICES, null=True)
    text_address = models.CharField(max_length=20, null=True)
    status =  models.CharField(max_length=20, choices = STATUS_CHOICES, default='TaskPosted')


    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    worker_decision = models.CharField(max_length=100,choices=DECISION_CHOICES, default="Pending")
