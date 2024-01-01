from django.http import JsonResponse
from .models import TaskNotification
from django.core.mail import send_mail
from rest_framework import viewsets,status
from .models import TaskNotification
from .serializers import TaskNotificationSerializer
from user.models import Client, Worker


class NotificationsViewSet(viewsets.ModelViewSet):
    
    queryset = TaskNotification.objects.all()
    serializer_class = TaskNotificationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Send email and text message
        #self.send_email_and_text(serializer.validated_data)
        
        self.perform_create(serializer)
        
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            task_notification = self.get_object()
        except TaskNotification.DoesNotExist:
            return JsonResponse({"message": "Task notification not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskNotificationSerializer(task_notification, data=request.data)
        if serializer.is_valid():
            # Update worker_decision
            task_notification.worker_decision = serializer.validated_data['worker_decision']

            if task_notification.worker_decision == 'Accept':
                ## create task object 
                
                ## create taskfeedback object based on task.id
                
                ## place the task.id generated from creating atsk object into the current task notification object.
                JsonResponse({"message": "Worker has accpeted your task offer"})
                
            elif task_notification.worker_decision == 'Reject':
                # Delete the TaskNotification if the worker rejects
                task_notification.delete()

            # No need to save after deletion
            return JsonResponse({"message": "This worker has rejected your task offer."})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def send_email_and_text(self, data):
        worker = data['receiver']
        
        # Send Email
        subject = 'New Task For you'
        message = f'You have a new task notification. Task: {data["task"].title}'
        from_email = 'shahood.bin.amir@gmail.com'  # replace with your email
        #to_email = worker.user.email  # assuming email is stored in the user model
        to_email = 'shahood.bin.amir@gmail.com'  # assuming email is stored in the user model
        
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        
        # Send Text Message (using Twilio)
        twilio_account_sid = 'your_account_sid'
        twilio_auth_token = 'your_auth_token'
        twilio_phone_number = 'your_twilio_phone_number'
        
        client = Client(twilio_account_sid, twilio_auth_token)
        
        # Assuming worker's phone number is stored in the user model
        to_phone_number = worker.user.phone_number
        
        if to_phone_number:
            message = client.messages.create(
                body=f'You have a new task notification. Task: {data["task"].title}',
                from_=twilio_phone_number,
                to=to_phone_number
            )