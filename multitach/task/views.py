from urllib import response
from user.serializers import ClientSerializer
from .serializers import TaskSerializer, TaskSerializer2
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets

    
from django.http import JsonResponse
from user.models import CustomUser, Client, Worker
import jwt

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from task.models import Task


import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

import os

from django.http import JsonResponse

# Get the absolute path to the task_classifier.pkl file
#model_path = os.path.abspath("AI-models/TaskPrediction/task_predictor.pkl")
model_path = os.path.join(os.path.dirname(__file__), 'task_predictor.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'tfidf_vectorizer.pkl')


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    


@api_view(['GET'])
def recommended_workers(request):

    if request.method == "GET":
        # Check if the user has logged-In        
        token = request.GET.get('jwt')
        rtask_title = request.GET.get('title')
        rtask_description = request.GET.get('description')
        
        if not token:
            return JsonResponse({"message": "You are not logged-In", "IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # if the session time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Session Expired", "IsUserLoggedIn": False})

        """ Our data coming form the API """

        rclient_id = payload['id']
        rworker_id = None

        # Load the pre-trained model and vectorizer
        classifier = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        if classifier is None:
            return JsonResponse({"message": "The classifier is absent"})

        if vectorizer is None:
            return JsonResponse({"message": "The vectorizer is absent"})

        # Use the text classification model to predict taskType
        text_tfidf = vectorizer.transform([rtask_description])
        rtask_type = classifier.predict(text_tfidf)[0]

        # Query workers with matching workerType and get the top three with the highest score
        workers_list = Worker.objects.filter(workerType=rtask_type).order_by('-base_rating')[:3]

        if workers_list.exists():
            # Extract information about the top three workers
            top_workers_info = [{
                                "worker_id": worker.id,
                                "userame": worker.user.username,
                                "user_id":worker.user.id,
                                "base_rating": worker.base_rating,
                                "Gigs Completed:":worker.task_count,
                                "Phone Number":worker.user.phone
                                }
                                for worker in workers_list]
            
            return JsonResponse({
                                "message": "Your request has been processed these are the results based on your title and description",
                                "task_type":rtask_type,
                                "task title":rtask_title,
                                "task description":rtask_description,
                                "client_id": rclient_id,
                                "worker_id": rworker_id,
                                "top_workers": top_workers_info})
        else:
            return JsonResponse({"message": "No matching worker found for the given task type"})



    # if request.method == "GET":
        #Check if the user has logged-In
        
        token = request.GET.get('jwt')
        
        if not token:
            return JsonResponse( {"message": "You are not logged-In","IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        #if the sessionn time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message": "Session Expired" , "IsUserLoggedIn": False })
          
        """ Our data coming form the API """
        
        rclient_id =  payload['id']
        rworker_id = None
        rtask_title = request.data.get('title')
        rtask_description = request.data.get('description')
        
        # Load the pre-trained model and vectorizer
        classifier = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        if classifier is None:
            return JsonResponse({"message": "The classifier is absent"})
        
        if vectorizer is None:
            return JsonResponse({"message": "The vectorizer is absent"})    
        
        # Use the text classification model to predict taskType
        text_tfidf = vectorizer.transform([rtask_description])
        rtask_type = classifier.predict(text_tfidf)[0]
        
        # Query workers with matching workerType and get the one with the highest score
        workers_list = Worker.objects.filter(workerType=rtask_type).order_by('base_rating')
        
        if workers_list.exists():
            selected_worker = workers_list.first()
            rworker_id = selected_worker.id

        else:
            return JsonResponse({"message": "No matching worker found for the given task type"})
    
    return JsonResponse()    
    
# only a client can post a task. 
@api_view(['POST'])
def post_a_task(request):
    
    if request.method == "POST":
        #Check if the user has logged-In
        
        token = request.GET.get('jwt')
        
        if not token:
            return JsonResponse( {"message": "You are not logged-In","IsUserLoggedIn": False})
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        #if the sessionn time is over.
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message": "Session Expired" , "IsUserLoggedIn": False })
          
        """ Our data coming form the API """
        
        rclient_id =  payload['id']
        rworker_id = None
        rtask_title = request.data.get('title')
        rtask_description = request.data.get('description')
        rtask_time = request.data.get('time')
        rtask_address_long = request.data.get('longitude')
        rtask_address_lat = request.data.get('latitude')
        
        # Load the pre-trained model and vectorizer
        classifier = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        if classifier is None:
            return JsonResponse({"message": "The classifier is absent"})
        
        if vectorizer is None:
            return JsonResponse({"message": "The vectorizer is absent"})    
        
        # Use the text classification model to predict taskType
        text_tfidf = vectorizer.transform([rtask_description])
        rtask_type = classifier.predict(text_tfidf)[0]
        
        # Query workers with matching workerType and get the one with the highest score
        workers_list = Worker.objects.filter(workerType=rtask_type).order_by('base_rating')
        
        if workers_list.exists():
            selected_worker = workers_list.first()
            rworker_id = selected_worker.id

        else:
            return JsonResponse({"message": "No matching worker found for the given task type"})
        
        task_data = {
            'client': rclient_id,
            'worker': rworker_id,
            'title': rtask_title,
            'description': rtask_description,
            'taskType': rtask_type,
            'time': rtask_time,
            'address': {
                'lat': rtask_address_lat,
                'long': rtask_address_long
            }
        }
        # return JsonResponse({"task": task_data})
        serializer = TaskSerializer(data=task_data)

        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse({"message": "Task created successfully", "task_id": serializer.data})
        else:
            return JsonResponse({"message": "Task creation failed", "errors": serializer.errors, "Task Details": serializer.data})
        
            
@api_view(['DELETE'])
def delete_a_task(request):
    if request.method == "DELETE":
        #Check if the user has logged-In
        token = request.GET.get('jwt')
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
        token = request.GET.get('jwt')
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
        task.time = request.data.get('time')
        task.address.long = request.data.get('longitude')
        task.address.lat = request.data.get('latitude')
        
        task.save()
        
        stask = TaskSerializer(task)
        return JsonResponse({"meesage": "task updated!" , "updated fields": stask.data})        
    
    
@api_view(['GET'])
def tasks_list(request):
    if request.method == 'GET':
        
        # Check if the user has logged-In
        token = request.GET.get('jwt')
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
        task = Task.objects.filter(client = client_id)
        stask = TaskSerializer(task,many=True)
        
        return JsonResponse({"message": "List of Tasks posted by this client.", "tasks": stask.data })            