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
                
        rclient_id = payload['id']        
        rworker_id = request.data.get('worker_id')        
    
    
    
    