from datetime import datetime, timedelta
from .serializers import ClientSerializer,WorkerSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
    
from django.http import JsonResponse
from user.models import CustomUser, Client, Worker
import jwt

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated




@api_view(['POST'])
def Login(request):
    if request.method == 'POST':
        remail = request.data.get('email')
        rpassword = request.data.get('password')
            
        # Query the CustomUser model to find a user with the provided email
        custom_user = CustomUser.objects.filter(email=remail).first()
            
        if custom_user is None:
            return JsonResponse({'message': 'Client not found'})
            
        # Check the password for the CustomUser
        if not custom_user.check_password(rpassword):
            return JsonResponse({"message": "Password is Incorrect"})

        # If the CustomUser exists, check if it has a related Client
        try:
            client = custom_user.client
        except Client.DoesNotExist:
            return JsonResponse({'message': 'Client not found'})
        
        payload = {
            'id' : client.id,                                           # client_id
            'exp': datetime.utcnow() + timedelta(minutes=60),    # expiry date of token
            'iat': datetime.utcnow()                           # token time creation
        }    
        
        token = jwt.encode(payload,'secret', algorithm='HS256')
        
        response = JsonResponse({'jwt': token})
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response

            
api_view(['GET'])
@permission_classes([IsAuthenticated])
def clientprofile(request):
    if request.method == 'GET':
        #token = request.COOKIES.get('jwt')
        token = request.data.get('jwt')
        # token = request.auth
        if not token:
            return JsonResponse( {"message":"Un authenticated"} )
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message":"Unauthenticated Session Expired"} )
        
        client = Client.objects.filter(id = payload['id']).first()
        sclient = ClientSerializer(client)
            
    return JsonResponse(sclient.data) 


@api_view(['POST'])
def Worker_Login(request):
    if request.method == 'POST':
        remail = request.data.get('email')
        rpassword = request.data.get('password')
            
        # Query the CustomUser model to find a user with the provided email
        custom_user = CustomUser.objects.filter(email=remail).first()
            
        if custom_user is None:
            return JsonResponse({'message': 'Client not found'})
            
        # Check the password for the CustomUser
        if not custom_user.check_password(rpassword):
            return JsonResponse({"message": "Password is Incorrect"})

        # If the CustomUser exists, check if it has a related Worker object
        try:
            worker = custom_user.worker
        except Worker.DoesNotExist:
            return JsonResponse({'message': 'Client not found'})
        
        payload = {
            'id' : worker.id,                                           # worker_id
            'exp': datetime.utcnow() + timedelta(minutes=60),    # expiry date of token
            'iat': datetime.utcnow()                           # token time creation
        }    
        
        token = jwt.encode(payload,'secret', algorithm='HS256')
        
        response = JsonResponse({'jwt': token})
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response

            
api_view(['GET'])
def WorkerProfile(request):
    if request.method == 'GET':
        token = request.COOKIES.get('jwt')
    
        if not token:
            return JsonResponse( {"message":"Un authenticated"} )
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message":"Unauthenticated Session Expired"} )
        
        worker = Worker.objects.filter(id = payload['id']).first()
        sworker = WorkerSerializer(worker)
            
    return JsonResponse(sworker.data) 

@csrf_exempt
@api_view(['POST'])
def Logout(request):
    if request.method == 'POST':
        response = JsonResponse({
            'message': 'User Logout Successfully.'
        })
        response.delete_cookie('jwt')
        return response


@api_view(['PUT'])
def update_client(request):
    if request.method == 'PUT':
        token = request.COOKIES.get('jwt')
    
        if not token:
            return JsonResponse( {"message":"Un authenticated"} )
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message":"Unauthenticated Session Expired"} )
            
        try:
            client = Client.objects.filter(id = payload['id']).first()
            
        except Client.DoesNotExist:
            return JsonResponse({"detail": "Worker not found"})

        # Extract only the fields you want to update from the request data
        update_data = {
            'user': {
                'image_url': request.data.get('user', {}).get('image_url'),
                'date_of_birth': request.data.get('user', {}).get('date_of_birth'),
                'gender': request.data.get('user', {}).get('gender'),
                'phone': request.data.get('user', {}).get('phone'),
            }
        }

        serializer = ClientSerializer(instance=client, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)

    
@api_view(['PUT'])
def update_worker(request):
    if request.method == 'PUT':
        token = request.COOKIES.get('jwt')
    
        if not token:
            return JsonResponse( {"message":"Un authenticated"} )
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message":"Unauthenticated Session Expired"} )
            
        try:
            worker = Worker.objects.filter(id = payload['id']).first()
            
        except Worker.DoesNotExist:
            return JsonResponse({"detail": "Worker not found"})

        # Extract only the fields you want to update from the request data
        update_data = {
            'user': {
                'username': request.data.get('user', {}).get('username'),
                'image_url': request.data.get('user', {}).get('image_url'),
                'date_of_birth': request.data.get('user', {}).get('date_of_birth'),
                'gender': request.data.get('user', {}).get('gender'),
                'phone': request.data.get('user', {}).get('phone'),
            },
            'workerLocation': request.data.get('workerLocation'),
            'workerType': request.data.get('workerType'),
        }

        serializer = WorkerSerializer(instance=worker, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)
    
@api_view(['GET'])
def unique_worker_types(request):
    if request.method == 'GET':
        # Use distinct to get unique worker types from the database
        unique_types = Worker.objects.values_list('workerType', flat=True).distinct()
        
        # Convert the query result to a list
        unique_types_list = list(unique_types)
        
        # Create a JSON response
        response_data = {'unique_worker_types': unique_types_list}
        
        return JsonResponse(response_data)