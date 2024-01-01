from .serializers import TaskNotificationSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from user.models import Client, Worker
from user.serializers import ClientSerializer, WorkerSerializer
import jwt
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .models import TaskNotification




# Define a function to send an email
def send_email(receiver_email, message):
    subject = 'New Task Notification'
    from_email = 'shahood.bin.amir@gmail.com'  # Set your email address
    send_mail(subject, message, from_email, [receiver_email])
    
    
@api_view(['POST'])
def create_task_notification(request):

    if request.method == 'POST':
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # if the session time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})
    
        sender = payload['id']
        receiver = request.data.get('receiver')
        rdescription = request.data.get('description')
        rtitle = request.data.get('title')
        #rworker_decision = request.data.get('rworker_decision')
        ris_read = request.data.get('is_read')
        
        rsender = Client.objects.get(id=sender)
        rreceiver = Worker.objects.get(id=receiver)
        
        sender_data = ClientSerializer(rsender).data
        receiver_data = WorkerSerializer(rreceiver).data
        
        send_email(rreceiver.user.email, "You have a new Task.")
        
        r_data = {
            'sender': sender_data['id'],
            'receiver': receiver_data['id'],
            'task': rtitle,
            'description': rdescription,
            'title': rtitle,
            'worker_decision': "Pending",
            'is_read': ris_read,
        }
        serializer = TaskNotificationSerializer(data=r_data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                                "message": "A task notification has been geenrated Sucessfully",
                                "data": r_data    
                                })
        else:
            return JsonResponse({"message": "Task Notification failed", "errors": serializer.errors, "Task Details": serializer.data})    


@api_view(['GET'])
def WorkerNotificationList(request):
    if request.method == "GET":
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            worker_id = payload['id']

            # Query to find all notification objects where worker_id is present
            notifications = TaskNotification.objects.filter(receiver = worker_id)

            # Serialize the notifications if needed
            serialized_notifications = TaskNotificationSerializer(notifications, many=True).data

            return JsonResponse({"message": "Notifications retrieved successfully", "notifications": serialized_notifications})
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})

@api_view(['POST'])
def WorkerSeenTask(request):
    if request.method == "POST":
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        notification_id =  request.data.get('notification_id')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            # Query to find the notification object by notification_id
            try:
                notification = TaskNotification.objects.get(id=notification_id)
                # Update the is_read field to True
                notification.is_read = True
                notification.save()

                return JsonResponse({"message": "Notification marked as read successfully"})
            
            except TaskNotification.DoesNotExist:
                return JsonResponse({"message": "Notification not found"}, status=404)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})
    if request.method == "POST":
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        notfication_id =  request.data.get('notification_id')
        
        ##query to find the notification object whose id is notfication_id and change the is_read from False to True.
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})                
        
@api_view(['GET'])
def ClientNotificationList(request):
    if request.method == "GET":
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # if the session time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})        

@api_view(['PUT'])
def WorkerAcceptTask(request):
    if request.method == "PUT":
        # Check if the user has logged-In        
        token = request.COOKIES.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # if the session time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})     
               
        # Get data from request body
        notification_id = request.data.get('notification_id')

        try:
            # Retrieve the notification object
            notification = TaskNotification.objects.get(pk=notification_id)

            # Check if the worker is not one who is making task reuest in the form of worker.
            #if request.worker.worker == notification.receiver:
                # Update worker decision to Accept
            notification.worker_decision = 'Accept'
            notification.save()

                # Return success message
            return JsonResponse({"message": "Task has been accepted successfully by the worker"})
            #else:
                # Return error message if user is not authorized
                #return JsonResponse({"message": "You are not authorized to accept this task"})
        except TaskNotification.DoesNotExist:
            # Return error message if notification does not exist
            return JsonResponse({"message": "Invalid notification ID"})

    # Return error message for other request methods
    return JsonResponse({"message": "Invalid request method"}, status=405)

    




