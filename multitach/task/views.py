from user.serializers import ClientSerializer
from .serializers import TaskSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
    
from django.http import JsonResponse
from user.models import CustomUser, Client, Worker
import jwt

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from task.models import Task

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
 
@api_view(['POST'])
def post_a_task(request):
    if request.method == "POST":
        #Check if the user has logged-In
        token = request.COOKIES.get('jwt')
        if not token:
            authentication = False
            return JsonResponse( {"message": "You are not logged-In","IsUserLoggedIn": authentication})
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        #if the sessionn time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message": "Session Expired" , "IsUserLoggedIn": authentication })
          
        """ Our data coming form the API """
        client_id =  payload['id']
        worker_id = request.data.get('worker_id')
        rtask_title = request.data.get('title')
        rtask_description = request.data.get('description')
        rtask_type = request.data.get('type')        
        rtask_time = request.data.get('time')
        rtask_address_long = request.data.get('longitude')
        rtask_address_lat = request.data.get('latitude')
        
        task_data = {
            'client': client_id,
            'worker': worker_id,
            'title': rtask_title,
            'description': rtask_description,
            'taskType': rtask_type,
            'time': rtask_time,
            'address': {
                'lat': rtask_address_lat,
                'long': rtask_address_long
            }
        }

        serializer = TaskSerializer(data=task_data)

        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse({"message": "Task created successfully", "task_id": task.id})
        else:
            return JsonResponse({"message": "Task creation failed", "errors": serializer.errors})
        
        
        
            
@api_view(['DELETE'])
def delete_a_task(request):
    if request.method == "DELETE":
        #Check if the user has logged-In
        token = request.COOKIES.get('jwt')
        if not token:
            authentication = False
            return JsonResponse( {"message": "You are not logged-In","IsUserLoggedIn": authentication})
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        #if the sessionn time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message": "Session Expired" , "IsUserLoggedIn": authentication })
          
        """ Our data coming form the API """
        client_id =  payload['id']
        task_id = request.data.get('task_id')
        
        try:
            # Try to get the task by its ID
            task = Task.objects.get(pk=task_id)
            
        except Task.DoesNotExist:
            isTask = False
            return JsonResponse({"message":"Task_ID invalid", "isTaskFound": isTask})

        """If the status of the task has been moved from the 'TaskPost' it cannot be deleted."""
          
        if task.status != 'TaskPosted':
             return JsonResponse({"message": "You cannot avail this option now.","TaskStatus": task.status})
        
        #check if the     
        if task.client.id != client_id:
            return JsonResponse({"message": "You don't have permission to delete this task."}, status=403)

        task.delete()
        
        return JsonResponse({"message": "Task Deleted Succesfully."})
        
        

        

@api_view(['PATCH'])
def update_a_task(request):
    if request.method == 'PATCH':
        #Check if the user has logged-In
        token = request.COOKIES.get('jwt')
        if not token:
            authentication = False
            return JsonResponse( {"message": "You are not logged-In","IsUserLoggedIn": authentication})
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        #if the sessionn time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message": "Session Expired" , "IsUserLoggedIn": authentication })
          
        """ Our data coming form the API """
        client_id =  payload['id']
        task_id = request.data.get('task_id')
        
        try:
            # Try to get the task by its ID
            task = Task.objects.get(pk=task_id)
            
        except Task.DoesNotExist:
            isTask = False
            return JsonResponse({"message":"Task_ID invalid", "isTaskFound": isTask})
        """If the status of the task has been moved from the 'TaskPost' it cannot be Updated."""
          
        if task.status != 'TaskPosted':
             return JsonResponse({"message": "You cannot avail this option now."})
        
        #check if the     
        if task.client.id != client_id:
            return JsonResponse({"message": "You don't have permission to delete this task."}, status=403)

        """Enter the new values for the Fields"""
        task.title = request.data.get('title')
        task.description = request.data.get('description')
        task.taskTyoe = request.data.get('type')        
        task.time = request.data.get('time')
        task.address.long = request.data.get('longitude')
        task.address.lat = request.data.get('latitude')
        
        task.save()
        
        return JsonResponse()        