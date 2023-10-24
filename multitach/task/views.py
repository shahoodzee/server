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
        
        client = Client.objects.filter(id = payload['id']).first()
        worker = Worker.objects.filter(id = worker_id).first()  #no authentication for worker_id it will come authenticated from the front-end.


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
        
        
    