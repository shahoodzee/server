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
        
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='received_notifications')
    description = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    worker_decision = models.CharField(max_length=100,choices=DECISION_CHOICES, default="Pending")
